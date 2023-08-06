import asyncio
import logging
import signal
import sys
import time
from typing import List, Dict, Callable, Optional, Any

import pyles
from pyles.logger import TelesFormatter, TelesHandler

class TelesApp(pyles.EventCallback):
    '''Base class of a python teles app'''
    def __init__(self, name: str, in_type: str, is_client: bool=False,
            recvlog: bool=False, recvvalue: bool=True, site="teles"):
        super().__init__()
        self.name: str = name
        self.type: str = in_type
        self.is_client: bool = is_client
        self.recvlog: bool = recvlog
        self.recvvalue: bool = recvvalue
        self.site = site
        self.started: bool = False
        self.status: int = 0
        self.status_list: Dict[int, str] = {0: "IDLE"}
        self.loop = asyncio.get_event_loop()
        self.properties: Dict[str, pyles.Property] = {}
        self.commands: List[pyles.CommandDef] = []
        self.command_callback: Dict[str, Callable[..., None]] = {}
        self.create_command("shutdown", "", [], self.cleanup)
        self.network_setup()
        # IMPORTANT!!! these two lines must be added AFTER network_setup()
        # I spent 1.5 days to get it, but I still don't understand why.
        self.loop.add_signal_handler(signal.SIGINT, self.cleanup)
        self.loop.add_signal_handler(signal.SIGTERM, self.cleanup)
        self.logger_setup()

    def load_conf(self) -> None:
        self.confmgr = pyles.ConfManager()
        self.confmgr.load(self.name)
        for key, value in self.confmgr.get(self.name).items():
            try:
                self.properties[key].set_value_string(value)
            except KeyError:
                pass

    def network_setup(self) -> None:
        '''setup teles network'''
        self.network = pyles.Network(self)
        self.network.setName(self.name)
        self.network.setDefaultGroup(self.site)
        self.network.setRecvLog(self.recvlog)
        self.network.setClient(self.is_client)
        self.network.setRecvValue(self.recvvalue)
        self.network.setType(self.type)

    def logger_setup(self) -> None:
        '''setup logger format'''
        self.logger: logging.Logger = logging.getLogger(self.name)
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        formatter = TelesFormatter(fmt="[%(asctime)s] [%(name)s] [%(colorlvl)s] %(message)s")
        stdout_handler.setFormatter(formatter)
        teles_handler = TelesHandler(self)
        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(teles_handler)
        self.logger.setLevel(logging.DEBUG)

    def poll(self) -> None:
        while self.started and self.network.poll():
            self.network.recv()

    async def async_loop(self) -> None:
        '''check teles network availability'''
        self.poll()
        await self.onIdle()
        await asyncio.sleep(0.005)
        asyncio.create_task(self.async_loop())

    def start(self) -> None:
        '''start teles network'''
        self.started = True
        self.network_setup()
        self.network.start()
        self.loop.create_task(self.async_loop())

    def cleanup(self, *args) -> None:
        '''stop event loop and teles network'''
        print("Cleanup")
        self.loop.stop()
        self.network.stop()

    async def onIdle(self) -> None:
        pass

    def onEnter(self, peer: pyles.Peer) -> None:
        super().onEnter(peer)
        print(peer.name, "enter")
        properties_vec = list(self.properties.values())
        infopb = pyles.create_info(properties_vec, self.commands,
            self.status_list, self.status)
        msg = pyles.pb_to_zmsg(infopb)
        self.network.sendOne(msg, peer)

    def onExit(self, peer: pyles.Peer) -> None:
        super().onExit(peer)
        print(peer.name, "exit")

    def onProperty(self, peer: pyles.Peer, prop: pyles.Property) -> None:
        super().onProperty(peer, prop)

    def onPropertyCommand(self, peer: pyles.Peer, msg: pyles.PropertyChangePB) -> None:
        prop = self.properties.get(msg.name, None)
        if prop is None:
            self.logger.warning("Unknown msg {} from {}".format(msg.name, peer.name))
            return
        if not prop.writable:
            self.logger.warning("Prop {} is not writable".format(prop.name))
            return
        prop.update_from_pb(msg)
        prop.send_property()

    # def onCommand(self, peer: pyles.Peer, command: List[str]) -> None:
    def onCommand(self, peer: pyles.Peer, cmd: pyles.CommandPB) -> None:
        print("onCommand", cmd)
        self.command_callback[cmd.cmd_name](*cmd.args)

    def create_property(self, propname: str, proptype: pyles.PropertyType,  desc: str='', writable: bool=False, egu: str='', init: Any=None) -> None:
        """Create property for the app
        :param str propname: Property name
        :param pyles.PropertyType proptype: Property type, enum of `pyles.PropertyType`
        :param str desc: Description
        :param bool writable: If the property can be modified externally
        :param init: init value for the property
        """
        if desc == '':
            desc = propname
        self.properties[propname] = pyles.Property(propname, proptype, desc, writable, self, egu)
        if init:
            self.setpropown(propname, init)

    def create_command(self, cmdname: str, desc: str, arglist: List[pyles.ArgDef],
            func: Callable[..., None]) -> None:
        cmddef: pyles.CommandDef = pyles.CommandDef()
        cmddef.name = cmdname
        cmddef.args = arglist
        cmddef.desc = desc
        self.commands.append(cmddef)
        self.command_callback[cmdname] = func

    def create_command_arg(self, argname: str, argtype: str) -> pyles.ArgDef:
        argtypeobj: pyles.ArgType = getattr(pyles.ArgType, argtype)
        return pyles.ArgDef(argtypeobj, argname)

    def change_status(self, value):
        if value not in self.status_list:
            return
        self.status = value
        self.network.sendStatus(value)

    def sendcmd(self, peer: pyles.Peer, *args: str) -> None:
        """Send command to other peer
        :param args: str lists, 0:cmd, 1:arg1, etc
        """
        if not peer.verify_command(args):
            raise Exception("Command format error")
        msg = pyles.pb_to_zmsg(pyles.genCommandPB(args))
        self.logger.debug("Will_sendcmd to {}: {}".format(peer.name, args))
        self.network.sendOne(msg, peer)

    def getpropown(self, propname: str) -> Any:
        return self.getprop(self, propname) # Although `self` is not instance/subclass of `pyles.Peer`

    def getprop(self, peer: pyles.Peer, propname: str) -> Any:
        if propname not in peer.properties:
            raise Exception("Property \"%s\" not found" % propname)
        prop: pyles.Property = peer.properties[propname]
        if prop.type == pyles.PropertyType.INT:
            return prop.get_value_int()
        if prop.type == pyles.PropertyType.DOUBLE:
            return prop.get_value_double()
        if prop.type == pyles.PropertyType.STRING:
            return prop.get_value_string()
        if prop.type == pyles.PropertyType.DOUBLE_LIST:
            return prop.double_list
        if prop.type == pyles.PropertyType.INT_LIST:
            return prop.int_list
        if prop.type == pyles.PropertyType.STR_LIST:
            return prop.str_list


    # TODO Set validator
    def setpropown(self, propname: str, val: Any) -> None:
        """Set property value of the application
        """
        self.properties[propname].set_value_string(str(val))

    list_types = ("double_list", "int_list", "str_list",)
    def setprop(self, peer: pyles.Peer, propname: str, val: Any) -> None:
        """Set peer's property value
        """
        prop = peer.properties[propname]
        prop.set_value_string(str(val))
        for typestr in TelesApp.list_types:
            if prop.type == getattr(pyles.PropertyType, typestr.upper()):
                setattr(peer, typestr, val)

        self.logger.debug("Will_setprop {}.{}={}".format(peer.name, propname, val))
        self.network.changeProperty(peer, prop)
