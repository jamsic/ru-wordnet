class Word:
    """Слово, состоящее из леммы и значения.

    Лемма -- это название статьи из Wiktionary, а определение -- одно из
    определений этого слова из статьи (только для русского языка).
    Например, для https://ru.wiktionary.org/wiki/медведь существуют 3 слова:
       - медведь, зоол. крупное мохнатое хищное млекопитающее (Ursus)
       ◆ Белый медведь крупнее бурого.
       - медведь, перен. сильный и крупный, но неуклюжий человек
       ◆ Отсутствует пример употребления (см. рекомендации).
       - медведь, перен., бирж. участник фондового рынка, играющий на понижение
       котировок акций ◆ Медведи продают акции с расчётом выкупить их потом
       подешевле, или просто продают, чтобы зафиксировать уже
       полученную прибыль.

    Методы:
        lemma (): возвращает лемму (название статьи Wiktionary).
        definition (): возвращает определение слова (только одно) в
        соответствии со статьей на Wiktionary
    """

    def __init__(self, word):
        self._lemma, self._definition = word

    def lemma(self):
        """Возвращает лемму.

        Args:
            нет

        Returns:
            строку - название статьи на Wiktionary.
        """
        return self._lemma

    def definition(self):
        """Возвращает определение слова.

        Args:
            нет

        Returns:
            строку - определение статьи на Wiktionary.
        """
        return self._definition

    def __eq__(self, other):
        return (self._lemma == other._lemma and
                self._definition == other._definition)

    def __hash__(self):
        return hash(self._lemma) + hash(self._definition)

    def __str__(self):
        str_ = '{0} {1}'
        return str_.format(self._lemma, self._definition)

