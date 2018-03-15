from django.http import JsonResponse
from rest_framework import generics, permissions, status, views
from . import serializers
from .scrapping import *


class NcdrcCaseHistoryAPIView(views.APIView):
    """
    Endpoint for Ncdrc CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(ncdrccasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class StateCommissionDelhiCaseHistoryAPIView(views.APIView):
    """
    Endpoint for StateCommission CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(statecommisiondelhicasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class CentralDelhiCaseHistoryAPIView(views.APIView):
    """
    Endpoint for CentralDelhi CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(centraldelhicasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class EastDelhiCaseHistoryAPIView(views.APIView):
    """
    Endpoint for EastDelhi CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(eastdelhicasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NewDelhiCaseHistoryAPIView(views.APIView):
    """
    Endpoint for NewDelhi CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(newdelhicasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NorthCaseHistoryAPIView(views.APIView):
    """
    Endpoint for North CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(northcasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NorthEastCaseHistoryAPIView(views.APIView):
    """
    Endpoint for NorthEast CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(northeastcasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)

class NorthWestCaseHistoryAPIView(views.APIView):
    """
    Endpoint for NorthWest CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(northwestcasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)

class SouthDelhiCaseHistoryAPIView(views.APIView):
    """
    Endpoint for SouthDelhi CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(southdelhicasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)

class South2CaseHistoryAPIView(views.APIView):
    """
    Endpoint for South2 CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(south2casehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class SouthWestCaseHistoryAPIView(views.APIView):
    """
    Endpoint for SouthWest CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(southwestcasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class WestDelhiCaseHistoryAPIView(views.APIView):
    """
    Endpoint for WestDelhi CaseHistory.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(westdelhicasehistory(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)

class NcdrcCaseStatusAPIView(views.APIView):
    """
    Endpoint for Ncdrc CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(ncdrccasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DelhiStateCommissionCaseStatusAPIView(views.APIView):
    """
    Endpoint for DelhiStateCommission CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(delhistatecommisioncasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)

class DistrictEastDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictEastDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districteastdelhicasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictSouthDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictSouthDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtsouthdelhicasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)

class DistrictWestDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictWestDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtwestdelhicasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictCentralDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictCentralDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtcentraldelhicasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNewDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictNewDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnewdelhicasestaus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNorthEastDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictNorthEastDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnortheastdelhicasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNorthWestDelhiCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictNorthWestDelhi CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnorthwestdelhicasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictSouth2CaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictSouth2 CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtsouth2casestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictSouthWestCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictSouthWest CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtsouthwestcasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNorthCaseStatusAPIView(views.APIView):
    """
    Endpoint for DistrictNorth CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnorthcasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NcdrcCaseJudgmentAPIView(views.APIView):
    """
    Endpoint for Ncdrc CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(ncdrcjudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DelhiStateCommissionJudgmentAPIView(views.APIView):
    """
    Endpoint for DelhiStateCommission CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(delhistatecommisionjudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictEastDelhiJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictEastDelhi CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districteastdelhijudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictSouthDelhiJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictSouthDelhi CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtsouthdelhijudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictWestDelhiJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictWestDelhi CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtwestdelhijudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictCentralDelhiJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictCentralDelhi CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtcentraldelhijudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNorthEastDelhiJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictNorthEastDelhi CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnortheastdelhijudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNorthWestDelhiJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictNorthWestDelhi CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnorthwestdelhijudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictSouth2JudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictSouth2 CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtsouth2judgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictSouthWestJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictSouthWest CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtsouthwestjudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class DistrictNorthJudgmentAPIView(views.APIView):
    """
    Endpoint for DistrictNorth CaseJudgment.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(districtnorthjudgment(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NcdrcOrderAPIView(views.APIView):
    """
    Endpoint for Ncdrc Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(ncdrcorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class StateCommisionOrderAPIView(views.APIView):
    """
    Endpoint for StateCommision Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(statecommisionorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class EastDelhiOrderAPIView(views.APIView):
    """
    Endpoint for EastDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(eastdelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class SouthDelhiOrderAPIView(views.APIView):
    """
    Endpoint for SouthDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(southdelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class WestDelhiOrderAPIView(views.APIView):
    """
    Endpoint for WestDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(westdelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class CentralDelhiOrderAPIView(views.APIView):
    """
    Endpoint for CentralDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(centraldelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NewDelhiOrderAPIView(views.APIView):
    """
    Endpoint for NewDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(newdelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NorthEastDelhiOrderAPIView(views.APIView):
    """
    Endpoint for NorthEastDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(northeastdelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NorthWestDelhiOrderAPIView(views.APIView):
    """
    Endpoint for NorthWestDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(northwestdelhiorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class South2OrderAPIView(views.APIView):
    """
    Endpoint for South2 Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(south2order(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class SouthWestOrderAPIView(views.APIView):
    """
    Endpoint for SouthWestDelhi Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(southwestorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class NorthOrderAPIView(views.APIView):
    """
    Endpoint for North Order.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(northorder(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class CgatNewCaseStatus(views.APIView):
    """
    Endpoint for CgatNew CaseStatus.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(cgatnewcasestatus(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class CgatNewCaseOrder(views.APIView):
    """
    Endpoint for CgatNew CaseOrder.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.NcdrcCasehistorySerializer

    def post(self, request):
        return JsonResponse(cgatneworders(casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)


class CgatNewCaseJudgment(views.APIView):
    """
    Endpoint for CgatNew CaseOrder.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.CgatNewJudgment

    def post(self, request):
        return JsonResponse(cgatnewjudgments(bench=request.data.get('bench'), casetype=request.data.get('casetype'), caseyear=request.data.get('caseyear'), caseno=request.data.get('caseno')), safe=False)
