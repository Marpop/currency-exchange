from rest_framework import serializers

from apps.nbp.choices import Currency


class ExchangeRateSerializer(serializers.Serializer):  # pylint: disable=abstract-method

    date = serializers.DateField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency_input = serializers.ChoiceField(choices=Currency.choices)
    currency_output = serializers.ChoiceField(choices=Currency.choices)

    class Meta:
        fields = [
            "date",
            "amount",
            "currency_input",
            "currency_output",
        ]

    def validate(self, attrs):
        if attrs["currency_input"] == attrs["currency_output"]:
            raise serializers.ValidationError(
                "Currency input and output cannot be the same."
            )
        return attrs
