from components.ability import AbilityComponent
from components.sectionName import SectionNameComponent
from components.topStats import TopStatsComponent
from components.trait import TraitComponent
from settings import *

from ui.newCard import NewCardUI


class EditCardUI(NewCardUI):
    def __init__(self, parent: object, statCard: object):
        super().__init__(parent)
        self.id = 'EditCardUI'
        self.title = 'Edit Card' 

        self.statCard: object = statCard

        self.components[0].buttonSelected = 'Token' if self.statCard.components[1].token else 'Standered'
        self.components[1].text = str(self.statCard.width)
        self.components[4].text = str(self.statCard.height)
        self.traits: int = 0
        self.abilities: int = 0
        for _comp in self.statCard.components:
            if isinstance(_comp, TraitComponent):
                self.traits += 1
            if isinstance(_comp, AbilityComponent):
                self.abilities += 1
        self.components[8].text = str(self.traits)
        self.components[12].text = str(self.abilities)

        for _comp in self.statCard.components:
            if isinstance(_comp, SectionNameComponent) and _comp.section == 'Traits':
                self.components[7].on = True
            elif isinstance(_comp, SectionNameComponent) and _comp.section == 'Abilities':
                self.components[11].on = True

        self.components[15].text = 'Edit'
        self.components[16].text = 'Cancel'

    def create(self):
        _top: TopStatsComponent = TopStatsComponent(self.statCard, self.components[0].buttonSelected == 'Token')
        _top.creatureSize = self.statCard.components[1].creatureSize
        _top.species = self.statCard.components[1].species
        _top.vigilance = self.statCard.components[1].vigilance

        _top.defense = self.statCard.components[1].defense
        _top.magicDefense = self.statCard.components[1].magicDefense
        _top.maxHP = self.statCard.components[1].maxHP
        _top.speed = self.statCard.components[1].speed

        _top.str = self.statCard.components[1].str
        _top.dex = self.statCard.components[1].dex
        _top.vit = self.statCard.components[1].vit
        _top.int = self.statCard.components[1].int
        _top.mnd = self.statCard.components[1].mnd
        self.statCard.components[1] = _top

        self.statCard.width = int(self.components[1].text)
        self.statCard.height = int(self.components[4].text)

        if len(self.statCard.components) >= 3 and not isinstance(self.statCard.components[2], SectionNameComponent):
            if self.components[7].on:
                self.statCard.components.insert(2, SectionNameComponent('Traits', 2, self.statCard))
        elif len(self.statCard.components) >= 3 and self.statCard.components[2].section != 'Traits':
            self.statCard.components.insert(2, SectionNameComponent('Traits', 2, self.statCard))

        if not isinstance(self.statCard.components[len(self.statCard.components) - 1 - self.abilities], SectionNameComponent):
            if self.components[11].on:
                self.statCard.components.insert(len(self.statCard.components) - self.abilities, SectionNameComponent('Abilities', 2, self.statCard))

        if self.components[7].on and int(self.components[8].text) >= self.traits:
            for _t in range(self.traits, int(self.components[8].text)):
                self.statCard.components.insert(3 + _t, TraitComponent(f'Trait {_t + 1}', '', self.statCard))

        if self.components[11].on and int(self.components[12].text) >= self.abilities:
            for _a in range(self.abilities, int(self.components[12].text)):
                self.statCard.components.append(AbilityComponent(f'Ability {_a + 1}', '', {}, self.statCard))

        _remove: list = []
        for _comp in self.statCard.components:
            if isinstance(_comp, SectionNameComponent):
                if _comp.section == 'Traits' and not self.components[7].on:
                    _remove.append(_comp)
                elif _comp.section == 'Abilities' and not self.components[11].on:
                    _remove.append(_comp)
            
            elif isinstance(_comp, TraitComponent):
                if not self.components[7].on:
                    _remove.append(_comp)

            elif isinstance(_comp, AbilityComponent):
                if not self.components[11].on:
                    _remove.append(_comp)

        for _r in _remove:
            self.statCard.components.remove(_r)

        self.parent.window = None                