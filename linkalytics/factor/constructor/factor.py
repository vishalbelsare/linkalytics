from abc import ABCMeta, abstractmethod

import collections

class FactorBase(metaclass=ABCMeta):
    """ Factor defines the abstract functions required for a factor.

        A factor implements two functions:
            lookup
            reverse_lookup

        One must also use `super(Foo, self).__init__(field_name)` to
        initialize the class. This records the field to be used in the
        factor.

        The `lookup` function takes an ad_id (as a string) as an
        argument, and returns a list of the field values for this
        factor.

        The `reverse_lookup` function takes a field value and returns a
        list of ad_ids matching (exactly) the same field value.

        For instance, if a database contains the following records

        id | email          | phone
        -- | -------------- | -----------
        0  | foo@bar.com    | 123 456 789
        1  | bar@baz.com    | 123 456 789

        Example
        -------

        .. code-block:: python

            >>> factor = Factor()
            >>> factor.lookup(0, "email")
            ["foo@bar.com"]
            >>> factor.lookup(1, "email")
            ["bar@baz.com"]
            >>> factor.reverse_lookup("email", "foo@bar.com")
            ["0"]
    """
    def suggest(self, ad_id, field, debug=False):
        """ The suggest function suggests other ad_ids that share this
            field with the input ad_id.

            If the debug field is set to True, this will ensure that the
            returned ad_ids *actually* match the field values. The debug
            option can be expensive to run, since it makes multiple
            calls to self.lookup.

            The number of calls to reverse_lookup is O(N) where N is
            the expected number of values in the field for this factor.
            This number is typically very small.

            If debugging, the expected number of calls to either
            reverse_lookup or lookup is O(N*M) where N is the expected
            number of values in the field for this factor and M is the
            expected number of ads matching this field.
        """
        field_values = self.lookup(ad_id, field)
        suggestions = {
            ad_id : {
                field: collections.defaultdict(list)
            }
        }
        if not isinstance(field_values, list):
            raise KeyError(field_values)

        for field_value in field_values:
            ads = set(self.reverse_lookup(field, field_value))
            try:
                ads.remove(ad_id)
            # Means that the reverse_lookup failed to find the originating ad itself.
            except KeyError:
                continue

            for x in ads:
                suggestions[ad_id][field][field_value].append(x)
            if debug:
                for x in ads:
                    assert field_value == self.lookup(x)

        return suggestions

    @abstractmethod
    def lookup(self, ad_id):
        """ lookup takes an ad_id (as a string) and returns a list of
            field values for self.field.
        """
        pass

    @abstractmethod
    def reverse_lookup(self, field_value):
        """ reverse_lookup takes a field value and returns a list of
            ad_ids for ads having field_value in self.field.
        """
        pass

