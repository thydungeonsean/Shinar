from ..pop_up import PopUp, TextPopUp


# Function Archive


# generic functions
def open_panel(self, id_key):
    try:
        self.layout.open_panel(id_key)

    except KeyError:
        raise Exception('Already Open')


def close_owner_panel(self):
    self.owner.delete()
    self.layout.refresh()


def switch_panel(self, id_key):

    open_panel(self, id_key)
    close_owner_panel(self)

# battle layout functions
#######################################


# panel opening functions
def open_command_panel(self):
    switch_panel(self, 'commands')


def open_disposition_panel(self):
    switch_panel(self, 'disposition_commands')


def open_general_panel(self):
    switch_panel(self, 'general_commands')


def open_infantry_panel(self):
    switch_panel(self, 'infantry_commands')


def open_archer_panel(self):
    switch_panel(self, 'archer_commands')


def open_chariot_panel(self):
    switch_panel(self, 'chariot_commands')


def open_infantry_disp(self):
    switch_panel(self, 'inf_disp')


def open_archer_disp(self):
    switch_panel(self, 'arch_disp')


def open_chariot_disp(self):
    switch_panel(self, 'char_disp')


# main button functions
def end_command_phase(self):
    command_phase = self.layout.state.scheduler.phase
    command_phase.end_phase()


# test
def make_pop_up(self):

    new = TextPopUp((40, 40), 100, 'Hi my name is Sean and I live in poop town this is a test this is only a test.')
    self.layout.add_element(new)


function_archive = {
    'close_owner': close_owner_panel,

    'back_command': open_command_panel,
    'back_disp': open_disposition_panel,

    'open_command': open_command_panel,
    'open_disp': open_disposition_panel,
    'open_inf_disp': open_infantry_disp,
    'open_arch_disp': open_archer_disp,
    'open_char_disp': open_chariot_disp,
    'open_general': open_general_panel,
    'open_infantry': open_infantry_panel,
    'open_archer': open_archer_panel,
    'open_chariot': open_chariot_panel,

    'end_command_phase': end_command_phase,

    'make_pop_up': make_pop_up,
}
