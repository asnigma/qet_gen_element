#!/usr/bin/env python3
# encoding: utf-8

# Imports
import logging as log
import re
# import xml.etree.ElementTree as etree  # python3-lxml
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
#from ElementTree_pretty import prettify

import uuid as uuidly
import math


class ElementCreate:

    def __init__(self, element_name, list_pin_name, pin_to_list, step, type_draw, file_path):
        self.file_path = file_path
        self.element_name = element_name
        self.pin_to_list = pin_to_list
        self.step = step
        self.type_draw = type_draw
        list_pin_name = list_pin_name.split(',')
        self.pin_name = []
        for pin in list_pin_name:
            pin = pin.strip()
            if pin.find('{') != -1:
                start = pin.find('{')
                stop = pin.find('}')
                name = pin[0:start]
                number = pin[start+1:stop]
                if number.find("z") != -1:
                    print(pin[start+2:stop])
                    number = int(pin[start+2:stop])
                    temp = 0
                else:
                    print(pin[start+1:stop])
                    number = int(pin[start+1:stop])
                    temp = 1
                
                for i in range(number):
                    n = i + temp
                    self.pin_name.append("{}{}".format(name, n))
            else:
                self.pin_name.append(pin)
        self.count_pin = len(self.pin_name)
        self.count_element = math.ceil(self.count_pin / pin_to_list)

        print("element_name = ", self.element_name, "self.pin_name = ", self.pin_name, "self.pin_to_list = ",
              self.pin_to_list, "self.step = ", self.step, "self.type_draw = ", self.type_draw)

    def _pin(self, father, x, y, diameter):
        ls = 'line-style:normal;line-weight:normal;filling:red;color:red'
        return SubElement(father, 'circle',
                          x=str(x-0.5*diameter), y=str(y-0.5*diameter), diameter=str(diameter),
                          antialias='false',
                          style=ls)

    def _rect(self, father, x, y, width, height, line_weight):
        style = 'line-style:normal;line-weight:{};filling:none;color:black'.format(
            line_weight)
        return SubElement(father, 'rect', antialias='false', ry="0", rx="0", x=str(x), y=str(y), width=str(width), height=str(height), style=style)

    def _circle(self, father, x, y, diameter):
        ls = 'line-style:normal;line-weight:normal;filling:none;color:black'
        return SubElement(father, 'circle',
                          x=str(x), y=str(y), diameter=str(diameter),
                          antialias='false',
                          style=ls)

    def _terminal(self, father, pin_name, x, y, orien):
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        return SubElement(father, 'terminal',
                          name=pin_name,
                          uuid=sUUID,
                          x=str(x), y=str(y),
                          orientation=orien
                          )

    def _label(self, father, text, x, y, size=4):
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        #font_size="Sans Serif,9,-1,5,50,0,0,0,0,0"
        font_size = "Sans Serif,{},-1,5,50,0,0,0,0,0".format(size)
        label = SubElement(father, 'dynamic_text',
                           text_width="-1",
                           uuid=sUUID,
                           Halignment="AlignLeft",
                           Valignment="AlignTop",
                           z="1",
                           frame="false",
                           text_from="UserText",
                           x=str(x),
                           y=str(y),
                           font=font_size,
                           rotation='0'
                           )
        label_text = SubElement(label, 'text')
        label_text.text = str(text)
        return label

    def _element_label(self, father, text, x, y, info_name, size=7):
        # element label
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        font_size = "Sans Serif,{},-1,5,50,0,0,0,0,0".format(size)
        label = SubElement(father, 'dynamic_text',
                           x=str(x),
                           y=str(y),
                           z='2',
                           text_from='ElementInfo',
                           text_width='-1',
                           uuid=sUUID,
                           font_size=font_size,
                           frame='false'
                           )
        label_text = SubElement(label, 'text')
        label_text.text = text
        label_info = SubElement(label, 'info_name')
        label_info.text = info_name
        return label

    def _line(self, father, x1, x2, y1, y2):
        ls = 'line-style:normal;line-weight:normal;filling:none;color:black'
        return SubElement(father, 'line',
                          x1=str(x1),
                          x2=str(x2),
                          y1=str(y1),
                          y2=str(y2),
                          length1='1.5',
                          length2='1.5',
                          end1='none',
                          end2='none',
                          antialias='false',
                          style=ls)

    def _vertical_divider(self, father, x, y):
        ls = 'line-style:normal;line-weight:thin;filling:none;color:black'
        return SubElement(father, 'polygon',
                          x1=str(0+x),
                          x2=str(0+x),
                          x3=str(-5+x),
                          x4=str(5+x),
                          x5=str(0+x),
                          x6=str(0+x),
                          y1=str(85+y),
                          y2=str(46+y),
                          y3=str(43+y),
                          y4=str(43+y),
                          y5=str(40+y),
                          y6=str(-5+y),
                          antialias="true",
                          closed="false",
                          style=ls
                          )

    def draw_pin(self, father, x, y, number_pin, name_pin, type_orientation):
        rect_width = 20
        rect_height = 10
        diam_pin = 3

        if type_orientation == 1:  # type_draw = Север
            x0 = x - 0.5*rect_width
            y0 = y
            x1 = x - 0.5*rect_width
            y1 = y + rect_height
            xt = x
            yt = y - 4
            orientation = "n"
        elif type_orientation == 2:  # type_draw = Запад
            x0 = x
            y0 = y - 0.5*rect_height
            x1 = x + rect_width
            y1 = y - 0.5*rect_height
            xt = x - 4
            yt = y
            orientation = "w"
        elif type_orientation == 3:  # type_draw = Восток
            x0 = x - rect_width
            y0 = y - 0.5*rect_height
            x1 = x - 2 * rect_width
            y1 = y - 0.5*rect_height
            xt = x + 4
            yt = y
            orientation = "e"
        else:  # type_draw = Юг
            x0 = x - 0.5*rect_width
            y0 = y - rect_height
            x1 = x - 0.5*rect_width
            y1 = y - 2 * rect_height
            xt = x
            yt = y + 4
            orientation = "s"

        self._rect(father, x0, y0, rect_width, rect_height, "thin")
        self._rect(father, x1, y1, rect_width, rect_height, "thin")
        self._terminal(father, name_pin, xt, yt, orientation)
        self._label(father, number_pin, x0, y0)
        self._label(father, name_pin, x1, y1)
        self._pin(father, x, y, diam_pin)


    def create_element_type1(self, pin, part):
        """
        |-------*-----------*-----------*-------|
        |       1           2           3       |
        |      P1          P2          P3       |
        |                                       |
        |_______________________________________|
        | name                                  |
        |_______________________________________|

        """
        total_height = 80
        total_width = 30 + self.step * (len(pin)-1) + 30
        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        definition = Element("definition",
                             height=str(total_height),
                             width=str(total_width),
                             hotspot_x='0',
                             hotspot_y='0',
                             link_type='simple',
                             orientation='dyyy',
                             version='0.8',
                             type='element')
        elementInformations = SubElement(definition, 'elementInformations')
        # Генерирование имени
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        uuid = SubElement(definition, 'uuid', uuid=sUUID)
        names = SubElement(definition, 'names')
        lang1 = SubElement(names, 'name', lang='en')
        lang1.text = label_name
        informations = SubElement(definition, 'informations')
        description = SubElement(definition, 'description')

        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        self._line(description, 0, total_width, 0, 0) 
        self._line(description, 0, total_width, total_height-20, total_height - 20)
        self._line(description, 0, total_width, total_height, total_height)

        self._label(description, label_name, 0, total_height - 20, size=7)
        self._element_label(description, "___", total_width+10, total_height - 20, "label")

        if (part == 1) and (self.count_element <= part):
            self._line(description, 0, 0, 0, total_height)
            self._line(description, total_width, total_width, 0, total_height)
        elif (part == 1) and (self.count_element > part):
            self._line(description, 0, 0, 0, total_height)
            self._vertical_divider(description, total_width, 0)
        elif (part > 1) and (self.count_element > part):
            self._vertical_divider(description, 0, 0)
            self._vertical_divider(description, total_width, 0)
        elif self.count_element == part:
            self._vertical_divider(description, 0, 0)
            self._line(description, total_width, total_width, 0, total_height)

        for i in range(len(pin)):
            x = 30+self.step*i
            y = 0
            number = i +1
            self.draw_pin(description, x, y, number, pin[i], 1)
        return definition

    def create_element_type2(self, pin, part):
        """
        |---------------------------------------|
        | name                                  |
        |---------------------------------------|
        |                                       |
        |      P1          P2          P3       |
        |       1           2           3       |
        |-------*-----------*-----------*-------|
        """ 
        total_height = 80
        total_width = 30 + self.step * (len(pin)-1) + 30
        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        definition = Element("definition",
                             height=str(total_height),
                             width=str(total_width),
                             hotspot_x='0',
                             hotspot_y='0',
                             link_type='simple',
                             orientation='dyyy',
                             version='0.8',
                             type='element')
        elementInformations = SubElement(definition, 'elementInformations')
        # Генерирование имени
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        uuid = SubElement(definition, 'uuid', uuid=sUUID)
        names = SubElement(definition, 'names')
        lang1 = SubElement(names, 'name', lang='en')
        lang1.text = label_name
        informations = SubElement(definition, 'informations')
        description = SubElement(definition, 'description')

        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        self._line(description, 0, total_width, 0, 0) 
        self._line(description, 0, total_width, 20, 20)
        self._line(description, 0, total_width, total_height, total_height)

        self._label(description, label_name, 0, 0, size=7)
        self._element_label(description, "___", total_width + 10, 0, "label")

        if (part == 1) and (self.count_element <= part):
            self._line(description, 0, 0, 0, total_height)
            self._line(description, total_width, total_width, 0, total_height)
        elif (part == 1) and (self.count_element > part):
            self._line(description, 0, 0, 0, total_height)
            self._vertical_divider(description, total_width, 0)
        elif (part > 1) and (self.count_element > part):
            self._vertical_divider(description, 0, 0)
            self._vertical_divider(description, total_width, 0)
        elif self.count_element == part:
            self._vertical_divider(description, 0, 0)
            self._line(description, total_width, total_width, 0, total_height)

        for i in range(len(pin)):
            x = 30+self.step*i
            y = total_height
            number = i +1
            self.draw_pin(description, x, y, number, pin[i], 4)
        return definition

    def create_element_type3(self, pin, part):
        """
        |-------------|
        | name        |
        |________     |
        * 1 | P1|     |
        |--------     |
        |________     |
        * 2 | P2|     |
        |--------     |
        |________     |
        * 3 | P3|     |
        |--------     |
        |_____________|
        
        """ 
        total_height = 30 + self.step * (len(pin)-1) + 30
        total_width = 80
        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        definition = Element("definition",
                             height=str(total_height),
                             width=str(total_width),
                             hotspot_x='0',
                             hotspot_y='0',
                             link_type='simple',
                             orientation='dyyy',
                             version='0.8',
                             type='element')
        elementInformations = SubElement(definition, 'elementInformations')
        # Генерирование имени
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        uuid = SubElement(definition, 'uuid', uuid=sUUID)
        names = SubElement(definition, 'names')
        lang1 = SubElement(names, 'name', lang='en')
        lang1.text = label_name
        informations = SubElement(definition, 'informations')
        description = SubElement(definition, 'description')

        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        self._line(description, 0, total_width, 0, 0)
        self._line(description, 0, total_width, total_height, total_height)
        self._line(description, 0, 0, 0, total_height)
        self._line(description, total_width, total_width, 0, total_height)

        self._element_label(description, "___", total_width+10, total_height - 20, "label")
        self._label(description, label_name, 0, 0, size=7)

        for i in range(len(pin)):
            x = 0
            y = 30+self.step*i 
            number = i +1
            self.draw_pin(description, x, y, number, pin[i], 2)
        return definition
 
    def create_element_type4(self, pin, part):
        """
        |-------------|
        | name        |
        |     ________|
        |     | P1| 1 *
        |     --------|
        |     ________|
        |     | P2| 2 *
        |     --------|
        |     ________|
        |     | P3| 3 *
        |     --------|
        |_____________|
        """ 
        total_height = 30 + self.step * (len(pin)-1) + 30
        total_width = 80
        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        definition = Element("definition",
                             height=str(total_height),
                             width=str(total_width),
                             hotspot_x='0',
                             hotspot_y='0',
                             link_type='simple',
                             orientation='dyyy',
                             version='0.8',
                             type='element')
        elementInformations = SubElement(definition, 'elementInformations')
        # Генерирование имени
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        uuid = SubElement(definition, 'uuid', uuid=sUUID)
        names = SubElement(definition, 'names')
        lang1 = SubElement(names, 'name', lang='en')
        lang1.text = label_name
        informations = SubElement(definition, 'informations')
        description = SubElement(definition, 'description')

        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        self._line(description, 0, total_width, 0, 0)
        self._line(description, 0, total_width, total_height, total_height)
        self._line(description, 0, 0, 0, total_height)
        self._line(description, total_width, total_width, 0, total_height)

        self._element_label(description, "___", total_width+10, total_height - 20, "label")
        self._label(description, label_name, 0, 0, size=7)

        for i in range(len(pin)):
            x = total_width
            y = 30+self.step*i 
            number = i +1
            self.draw_pin(description, x, y, number, pin[i], 3)
        return definition

    def create_element_type5(self, pin, part):
        """
        |-------------------|
        | name              |
        |______      _______|
        * 1 |P1|     |P2| 2 *
        |-------     -------|
        |                   |
        |______      _______|
        * 3 |P3|     |P4| 4 *
        |-------     -------|
        |___________________|
        """
        tm  = len(pin)//2 - 1 if len(pin)%2 == 0 else len(pin)//2 
        total_height = 30 + self.step * tm + 30
        total_width  = 10 + 20*4

        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        definition = Element("definition",
                             height=str(total_height),
                             width=str(total_width),
                             hotspot_x='0',
                             hotspot_y='0',
                             link_type='simple',
                             orientation='dyyy',
                             version='0.8',
                             type='element')
        elementInformations = SubElement(definition, 'elementInformations')
        # Генерирование имени
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        uuid = SubElement(definition, 'uuid', uuid=sUUID)
        names = SubElement(definition, 'names')
        lang1 = SubElement(names, 'name', lang='en')
        lang1.text = label_name
        informations = SubElement(definition, 'informations')
        description = SubElement(definition, 'description')

        self._line(description, 0, total_width, 0, 0)
        self._line(description, 0, total_width, total_height, total_height)
        self._line(description, 0, 0, 0, total_height)
        self._line(description, total_width, total_width, 0, total_height)

        self._element_label(description, "___", total_width+10, total_height - 20, "label")
        self._label(description, label_name, 0, 0, size=7)

        for i in range(len(pin)):
            if i % 2 == 0:
                x = 0
                orientation = 2
            else:
                x = total_width
                orientation = 3
            k = i // 2
            y = 0 + 30 + k * self.step
            number = i + 1
            self.draw_pin(description, x, y, number, pin[i], orientation)

        return definition

    def create_element_type6(self, pin, part):
        """
        |-------------------|
        | name              |
        |______      _______|
        * 1 |P1|     |P3| 3 *
        |-------     -------|
        |                   |
        |______      _______|
        * 2 |P2|     |P4| 4 *
        |-------     -------|
        |___________________|
        """        
        tm  = len(pin)//2 - 1 if len(pin)%2 == 0 else len(pin)//2 
        total_height = 30 + self.step * tm + 30
        total_width  = 10 + 20*4

        if self.count_element == 1:
            label_name = "{}".format(self.element_name)
        else:
            label_name = "{} part {}/{}".format(self.element_name, part, self.count_element)

        definition = Element("definition",
                             height=str(total_height),
                             width=str(total_width),
                             hotspot_x='0',
                             hotspot_y='0',
                             link_type='simple',
                             orientation='dyyy',
                             version='0.8',
                             type='element')
        elementInformations = SubElement(definition, 'elementInformations')
        # Генерирование имени
        sUUID = '{' + uuidly.uuid1().urn[9:] + '}'
        uuid = SubElement(definition, 'uuid', uuid=sUUID)
        names = SubElement(definition, 'names')
        lang1 = SubElement(names, 'name', lang='en')
        lang1.text = label_name
        informations = SubElement(definition, 'informations')
        description = SubElement(definition, 'description')

        self._line(description, 0, total_width, 0, 0)
        self._line(description, 0, total_width, total_height, total_height)
        self._line(description, 0, 0, 0, total_height)
        self._line(description, total_width, total_width, 0, total_height)

        self._element_label(description, "___", total_width+10, total_height - 20, "label")
        self._label(description, label_name, 0, 0, size=7)

        for i in range(len(pin)):
            if len(pin) / 2  > i:
                orientation = 2
                x = 0
                k = i 
                y = 0 + 30 + k * self.step
                number = i +1
            else:
                orientation = 3
                x = total_width
                k = i - len(pin) / 2   if len(pin)%2 == 0  else i - (len(pin)+1) / 2 
                y = 0 + 30 + k * self.step
                number = i +1
            self.draw_pin(description, x, y, number, pin[i], orientation)

        return definition


    def main(self):
        for i in range(self.count_element):
            part = i + 1
            start = i * self.pin_to_list
            stop = (i+1) * self.pin_to_list 
            if self.count_element !=1:
                file_name = "{}/{}_part{}.elmt".format(self.file_path, self.element_name, part)
            else:
                file_name = "{}/{}.elmt".format(self.file_path, self.element_name)
            if self.type_draw == 1:
                qet_element = self.create_element_type1(self.pin_name[start:stop], part)
            if self.type_draw == 2:
                qet_element = self.create_element_type2(self.pin_name[start:stop], part)
            if self.type_draw == 3:
                qet_element = self.create_element_type3(self.pin_name[start:stop], part)
            if self.type_draw == 4:
                qet_element = self.create_element_type4(self.pin_name[start:stop], part)
            if self.type_draw == 5:
                qet_element = self.create_element_type5(self.pin_name[start:stop], part)
            if self.type_draw == 6:
                qet_element = self.create_element_type6(self.pin_name[start:stop], part)

            mydata = str(tostring(qet_element))
            mydata = mydata[2: -1]           
            myfile = open(file_name, "w")
            myfile.write(mydata)

        return print("Create {}".format(file_name))


#ds = ElementCreate(element_name="ГЕРЕНАТОР", list_pin_name="COM+, I{25}, Q{28}, GND", pin_to_list=80, step=20, type_draw=1, file_path = "/home/nigma/Документы/QElectroTech_Librery/elements/" )
# for i in range(5):
#     print(ds.draw_pin(30+50*i, 0, i, "Q1.{}".format(i), 4))
# print(ds.draw_poligon(10, 0))
# print(ds.draw_dynamic_text("444444", 10, 0, "label"))
#wt = ds.main()
#mydata = str(tostring(wt))
#mydata = mydata[2: -1]
# print(mydata)
#myfile = open("items2.xml", "w")
# myfile.write(mydata)
# wt.write("output.xhtml")
