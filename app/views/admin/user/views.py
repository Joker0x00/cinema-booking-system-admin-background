# Author: wy
# Time: 2022/8/27 10:36

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.utils.response import Response
from app.utils.loadData import LoadJsonData


def get_user_info(request):
    # print(request.GET.get('token'))
    res = {
        'code': 200,
        'data': {
            "routes": [
                "A",
                "User",
                "Category",
                "Discount",
                "ActivityEdit",
                "CouponRule",
                "Product",
                "Activity",
                "CouponAdd",
                "Trademark",
                "Attr",
                "ActivityAdd",
                "Test3",
                "Test2",
                "CouponEdit",
                "OrderShow",
                "Test",
                "Permission",
                "Spu",
                "UserList",
                "ClientUser",
                "consumer",
                "Order",
                "Coupon",
                "test123321",
                "Banner",
                "Acl",
                "ActivityRule",
                "Role",
                "RoleAuth",
                "Test1",
                "Refund",
                "consumerlist",
                "OrderList",
                "Sku",
                "TradeMark"
            ],
            "buttons": [
                "cuser.detail",
                "cuser.update",
                "cuser.delete",
                "btn.User.add",
                "btn.User.remove",
                "btn.User.update",
                "btn.User.assgin",
                "btn.Role.assgin",
                "btn.Role.add",
                "btn.Role.update",
                "btn.Role.remove",
                "btn.Permission.add",
                "btn.Permission.update",
                "btn.Permission.remove",
                "btn.Activity.add",
                "btn.Activity.update",
                "btn.Activity.rule",
                "btn.Coupon.add",
                "btn.Coupon.update",
                "btn.Coupon.rule",
                "btn.OrderList.detail",
                "btn.OrderList.Refund",
                "btn.UserList.lock",
                "btn.Category.add",
                "btn.Category.update",
                "btn.Category.remove",
                "btn.Trademark.add",
                "btn.Trademark.update",
                "btn.Trademark.remove",
                "btn.Attr.add",
                "btn.Attr.update",
                "btn.Attr.remove",
                "btn.Spu.add",
                "btn.Spu.addsku",
                "btn.Spu.update",
                "btn.Spu.skus",
                "btn.Spu.delete",
                "btn.Sku.updown",
                "btn.Sku.update",
                "btn.Sku.detail",
                "btn.Sku.remove",
                "btn.Role.a",
                "btn.add1",
                "btn.add2",
                "btn.Add3",
                "btn.edit"
            ],
            "roles": [
                "普通员工"
            ],
            "name": "admin",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
        },
        'message': '成功登录',
        'success': True
    }
    return JsonResponse(res)


def login(request):
    data = LoadJsonData(request.body).get_data()
    res = {
        "success": True,
        "code": 20000,
        "message": "成功",
        "data": {
            "token": "eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJSSkzJzcxT0lFKrShQsjI0MzM0NTI2NTaqBQCV9puSIAAAAA.awM_i4jsrGgU7pJScZ1LKGy2Es82oMa23WezBKAKeDjO27-yccTC_nTPkQmvQvB2_qrTK44GZEXRA9qb1mpD3Q"
        }
    }
    return JsonResponse(res)


def logout(request):
    res = {
        "success": True,
        "code": 200,
        "message": "成功",
        "data": {}
    }
    return JsonResponse(res)
