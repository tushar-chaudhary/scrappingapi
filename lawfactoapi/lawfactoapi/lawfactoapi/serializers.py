from rest_framework import serializers

class NcdrcCasehistorySerializer(serializers.Serializer):

    casetype = serializers.CharField(
        required=True, label="Case Type"
    )
    caseno   = serializers.CharField(
        required=True, label="Case Number"
    )
    caseyear = serializers.CharField(
        required=True, label="Case Year"
    )

    def validate_case(self, value):
        return value


class CgatNewJudgment(serializers.Serializer):

    bench = serializers.CharField(
        required=True, label="Bench"
    )

    casetype = serializers.CharField(
        required=True, label="Case Type"
    )
    caseno   = serializers.CharField(
        required=True, label="Case Number"
    )
    caseyear = serializers.CharField(
        required=True, label="Case Year"
    )

    def validate_case(self, value):
        return value

