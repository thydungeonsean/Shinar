from ...constants import FRAMES_PER_TURN
import battle_phase


class ActionPhase(battle_phase.BattlePhase):

    def __init__(self, owner):
        battle_phase.BattlePhase.__init__(self, owner, 'action')
        self.tick = 0
        self.end_of_phase = FRAMES_PER_TURN

    def increment_tick(self):
        self.tick += 1

    def run(self):
        self.set_troop_actions()
        self.run_troop_actions()
        self.increment_tick()
        if self.tick >= self.end_of_phase:
            self.end_phase()

    def set_troop_actions(self):
        for troop in self.owner.ready_troops:
            new_action = self.owner.action_assigner.get_next_action(troop)
            self.owner.action_queue.append(new_action)
        del self.owner.ready_troops[:]

    def run_troop_actions(self):

        for action in self.owner.action_queue[:]:
            action.run()

    def end_phase_effects(self):
        print 'end of action phase'
        self.tick = 0
        if not self.owner.engagements.engagements:
            self.engage_all()

    def get_next_phase(self):
        if self.owner.engagements.engagements:
            next_phase = 'engagement'
            self.assign_engagement_actions()
        else:
            next_phase = 'action'
        return next_phase

    def engage_all(self):
        for troop in self.owner.battle.left_army.troops:
            if troop.state not in ('flee', 'rout'):
                target = self.owner.action_assigner.check_melee_target(troop)
                if target is not None:
                    # TODO need to find way to get supports to work here
                    self.owner.engagements.initiate_engagement(troop, target)

    def assign_engagement_actions(self):
        for engagement in self.owner.engagements.engagements:
            actions = self.owner.action_assigner.get_engagement_melees(engagement)
            self.owner.action_queue.extend(actions)
