#! /usr/bin/env python


from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_string import Property_String

from .base import Base


class Controller_Action(Base,Device_Base):

    def __init__(self, isy_device=None,homie_settings=None, mqtt_settings=None):

        Base.__init__ (self,isy_device)

        Device_Base.__init__ (self,self.get_homie_device_id(), isy_device.name, homie_settings, mqtt_settings)
        
        paddle_node = Node_Base(self,id='paddle',name='paddle',type_='paddle')
        self.add_node(paddle_node)

        self.paddle = Property_String(paddle_node,'paddle-action','Paddle Action')

        Device_Base.start(self)

    def property_change(self,property_,value):
        if property_ == 'paddle_action':
            self.paddle.value = value
            
        Base.property_change (self,property_,value)

