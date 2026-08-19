from pathlib import Path

path = Path(__file__).resolve().parent / 'Seminar11_OOP_UML_SENIOR_V11.py'
s = path.read_text(encoding='utf-8')
repls = []

repls.append((
'''    def uml_generalization(self, child: Mobject, parent: Mobject) -> VGroup:\n        """Hollow-triangle UML generalization from child to parent."""\n        start = child.get_top()\n        end = parent.get_bottom()\n''',
'''    def uml_generalization(self, child: Mobject, parent: Mobject, target_shift=ORIGIN, start_shift=ORIGIN) -> VGroup:\n        """Hollow-triangle UML generalization with explicit child/parent anchors."""\n        start = child.get_top() + start_shift\n        end = parent.get_bottom() + target_shift\n'''))

repls.append((
'''    def uml_realization(self, child: Mobject, interface: Mobject) -> VGroup:\n        """Dashed UML realization with a hollow triangular tip."""\n        start = child.get_top()\n        end = interface.get_bottom()\n''',
'''    def uml_realization(self, child: Mobject, interface: Mobject, target_shift=ORIGIN, start_shift=ORIGIN) -> VGroup:\n        """Dashed UML realization with distinct anchors for legible fan-out."""\n        start = child.get_top() + start_shift\n        end = interface.get_bottom() + target_shift\n'''))

repls.append((
'''    def uml_composition(self, owner: Mobject, part: Mobject, label: str = "") -> VGroup:\n        """UML composition: filled diamond at owner side plus a non-crossing connector."""\n        start = owner.get_bottom()\n''',
'''    def uml_composition(self, owner: Mobject, part: Mobject, label: str = "", owner_shift=ORIGIN) -> VGroup:\n        """UML composition with a distinct filled-diamond anchor on the owner."""\n        start = owner.get_bottom() + owner_shift\n'''))

repls.append((
'''        label = self.text("INSTANTIATION", 18, BOLD).move_to(RIGHT*2.65 + UP*2.15)\n        arrows = VGroup(*[\n            Arrow(robot_class.get_right()+RIGHT*0.06, obj.get_left()+LEFT*0.08, buff=0.12, color=LIGHT_GRAY, stroke_width=1.7)\n            for obj in objects\n        ])\n        note = self.text("Same class. Different state.", 25, BOLD).to_edge(DOWN, buff=0.34)\n\n        layout = VGroup(robot_class, objects, label, arrows)\n''',
'''        label = self.text("UML OBJECT INSTANCES", 18, BOLD).move_to(RIGHT*2.65 + UP*2.15)\n        note = self.text("Same class. Different state.", 25, BOLD).to_edge(DOWN, buff=0.34)\n\n        layout = VGroup(robot_class, objects, label)\n'''))

repls.append((
'''        self.play(FadeIn(label), run_time=RUN_QUICK)\n        for obj, arrow in zip(objects, arrows):\n            self.play(GrowArrow(arrow), FadeIn(obj, shift=UP*0.08), run_time=RUN_NORMAL)\n''',
'''        self.play(FadeIn(label), run_time=RUN_QUICK)\n        for obj in objects:\n            self.play(FadeIn(obj, shift=UP*0.08), run_time=RUN_NORMAL)\n'''))

old_inheritance = '''        parent = self.uml_class(\n            "Vehicle",\n            ["# speed : float", "# position : float"],\n            ["+ move()", "+ stop()"],\n            width=4.15, height=3.20, title_size=27, body_size=18,\n        ).move_to(UP*0.92)\n        robot = self.uml_class(\n            "Robot",\n            ["- energy : int"],\n            ["+ recharge()"],\n            width=4.25, height=2.70, title_size=25, body_size=18,\n        ).move_to(LEFT*3.65 + DOWN*2.15)\n        drone = self.uml_class(\n            "Drone",\n            ["- altitude : float"],\n            ["+ take_off()"],\n            width=4.25, height=2.70, title_size=25, body_size=18,\n        ).move_to(RIGHT*3.65 + DOWN*2.15)\n        relations = VGroup(self.uml_generalization(robot, parent), self.uml_generalization(drone, parent))\n'''
new_inheritance = '''        parent = self.uml_class(\n            "Vehicle",\n            ["# speed : float", "# position : float"],\n            ["+ move()", "+ stop()"],\n            width=4.15, height=2.80, title_size=27, body_size=18,\n        ).move_to(UP*1.07)\n        robot = self.uml_class(\n            "Robot",\n            ["- energy : int"],\n            ["+ recharge()"],\n            width=4.25, height=2.45, title_size=25, body_size=18,\n        ).move_to(LEFT*3.65 + DOWN*2.00)\n        drone = self.uml_class(\n            "Drone",\n            ["- altitude : float"],\n            ["+ take_off()"],\n            width=4.25, height=2.45, title_size=25, body_size=18,\n        ).move_to(RIGHT*3.65 + DOWN*2.00)\n        relations = VGroup(\n            self.uml_generalization(robot, parent, LEFT*1.35, RIGHT*1.55),\n            self.uml_generalization(drone, parent, RIGHT*1.35, LEFT*1.55),\n        )\n'''
repls.append((old_inheritance, new_inheritance))

repls.append((
'''        relations = VGroup(*[self.uml_realization(c, interface) for c in classes])\n''',
'''        relations = VGroup(\n            self.uml_realization(robot, interface, LEFT*1.20, RIGHT*1.55),\n            self.uml_realization(drone, interface, ORIGIN, ORIGIN),\n            self.uml_realization(boat, interface, RIGHT*1.20, LEFT*1.55),\n        )\n'''))

repls.append((
'''        relations = VGroup(\n            self.uml_composition(whole, inventory),\n            self.uml_composition(whole, robot),\n            self.uml_composition(whole, sensor),\n        )\n''',
'''        relations = VGroup(\n            self.uml_composition(whole, inventory, owner_shift=LEFT*0.62),\n            self.uml_composition(whole, robot, owner_shift=ORIGIN),\n            self.uml_composition(whole, sensor, owner_shift=RIGHT*0.62),\n        )\n'''))

old_project = '''        scenario = self.text("Smart garden: read soil moisture and activate a pump when water is needed.", 24, BOLD).move_to(UP*2.25)\n        controller = self.uml_class("Controller", ["- threshold : float"], ["+ evaluate()"], width=3.75, height=2.55, body_size=16).move_to(UP*0.60)\n        sensor = self.uml_class("MoistureSensor", ["- value : float"], ["+ read()"], width=3.75, height=2.55, body_size=16).move_to(LEFT*4.45 + DOWN*2.05)\n        pump = self.uml_class("Pump", ["- isOn : bool"], ["+ start()", "+ stop()"], width=3.75, height=2.55, body_size=16).move_to(DOWN*2.05)\n        garden = self.uml_class("Garden", ["- name : str"], ["+ irrigate()"], width=3.75, height=2.55, body_size=16).move_to(RIGHT*4.45 + DOWN*2.05)\n        classes = VGroup(controller, sensor, pump, garden)\n\n        sensor_link = Arrow(sensor.get_top()+UP*0.02, controller.get_left()+DOWN*0.18, buff=0.12, color=BLACK_LINE, stroke_width=1.8)\n        sensor_label = self.text("moisture", 16, MEDIUM).move_to((sensor_link.get_start()+sensor_link.get_end())/2 + LEFT*0.18)\n        pump_link = Arrow(controller.get_bottom()+DOWN*0.02, pump.get_top()+UP*0.02, buff=0.12, color=BLACK_LINE, stroke_width=1.8)\n        pump_label = self.text("command", 16, MEDIUM).next_to(pump_link, RIGHT, buff=0.10)\n        garden_link = Arrow(controller.get_right()+DOWN*0.18, garden.get_top()+UP*0.02, buff=0.12, color=BLACK_LINE, stroke_width=1.8)\n        garden_label = self.text("decision", 16, MEDIUM).move_to((garden_link.get_start()+garden_link.get_end())/2 + RIGHT*0.18)\n        links = VGroup(VGroup(sensor_link, sensor_label), VGroup(pump_link, pump_label), VGroup(garden_link, garden_label))\n'''
new_project = '''        scenario = self.text("Smart garden: read soil moisture and activate a pump when water is needed.", 24, BOLD).move_to(UP*2.35)\n        controller = self.uml_class("Controller", ["- threshold : float"], ["+ evaluate()"], width=3.75, height=2.55, body_size=16).move_to(UP*0.85)\n        sensor = self.uml_class("MoistureSensor", ["- value : float"], ["+ read()"], width=3.75, height=2.55, body_size=16).move_to(LEFT*4.65 + DOWN*2.05)\n        pump = self.uml_class("Pump", ["- isOn : bool"], ["+ start()", "+ stop()"], width=3.75, height=2.55, body_size=16).move_to(DOWN*2.05)\n        garden = self.uml_class("Garden", ["- name : str"], ["+ irrigate()"], width=3.75, height=2.55, body_size=16).move_to(RIGHT*4.65 + DOWN*2.05)\n        classes = VGroup(controller, sensor, pump, garden)\n\n        # Classical UML-style associations: simple solid lines and labels in whitespace.\n        sensor_link = Line(sensor.get_top()+UP*0.02, controller.get_left()+DOWN*0.30, color=BLACK_LINE, stroke_width=1.8)\n        sensor_label = self.text("reads", 16, MEDIUM).move_to(sensor_link.get_center() + UP*0.32 + LEFT*0.05)\n        pump_link = Line(controller.get_bottom()+DOWN*0.02, pump.get_top()+UP*0.02, color=BLACK_LINE, stroke_width=1.8)\n        pump_label = self.text("controls", 16, MEDIUM).move_to(pump_link.get_center() + RIGHT*0.86 + UP*0.08)\n        garden_link = Line(pump.get_right()+UP*0.62, garden.get_left()+UP*0.62, color=BLACK_LINE, stroke_width=1.8)\n        garden_label = self.text("waters", 16, MEDIUM).move_to(garden_link.get_center() + UP*0.28)\n        links = VGroup(VGroup(sensor_link, sensor_label), VGroup(pump_link, pump_label), VGroup(garden_link, garden_label))\n'''
repls.append((old_project, new_project))

repls.append((
'''        for link in links:\n            self.play(GrowArrow(link[0]), FadeIn(link[1]), run_time=RUN_NORMAL)\n''',
'''        for link in links:\n            self.play(Create(link[0]), FadeIn(link[1]), run_time=RUN_NORMAL)\n'''))

# Senior QA Rev2: place UML instance underline below glyphs, never through text.
repls.append((
    "        underline = Line(header.get_left()+DOWN*0.07, header.get_right()+DOWN*0.07, color=BLACK_LINE, stroke_width=1.2)\n",
    "        underline_y = header.get_bottom()[1] - 0.07\n"
    "        underline = Line(\n"
    "            [header.get_left()[0], underline_y, 0],\n"
    "            [header.get_right()[0], underline_y, 0],\n"
    "            color=BLACK_LINE, stroke_width=1.2,\n"
    "        )\n",
))

# Senior QA Rev2: labels are independent layout blocks; they may not touch UML class boxes.
repls.append((
    "        self.assert_no_overlap([controller, sensor, pump, garden], \"scene_07 class boxes\")\n",
    "        self.assert_no_overlap([controller, sensor, pump, garden], \"scene_07 class boxes\")\n"
    "        self.assert_no_overlap(\n"
    "            [controller, sensor, pump, garden, sensor_label, pump_label, garden_label],\n"
    "            \"scene_07 boxes and association labels\",\n"
    "            padding=0.0,\n"
    "        )\n",
))

for old, new in repls:
    count = s.count(old)
    if count != 1:
        raise RuntimeError(f'Expected exactly one patch target, found {count}: {old[:100]!r}')
    s = s.replace(old, new)

path.write_text(s, encoding='utf-8')
print('V11 visual QA patch v3 / Senior QA Rev2 applied')
