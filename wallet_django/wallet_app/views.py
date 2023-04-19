from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .wallet import get_wallet
from datetime import datetime
from .models import Master, Address


def index(request):
    return render(request, "index.html") 


def generate_master(request, coin):
    now = datetime.now()
    wallet = get_wallet(coin)
    if wallet == None:
        response = {'status': 'error', 'timestamp': f'{now}', 'message': 'coin not supported'}
        return JsonResponse(response)
    count = Master.objects.filter(coin=coin).count()
    if count > 0:
        response = {'status': 'error', 'timestamp': f'{now}', 'message': 'coin master already exist'}
        return JsonResponse(response)
    seed, private_key, chain_code = wallet.generate_master()
    master = Master(coin=coin, seed=seed, private_key=private_key, chain_code=chain_code)
    master.save()
    response = {'status': 'ok', 'timestamp': f'{now}', 'coin': f'{coin}', 'seed': f'{seed}', 
                'private_key': f'{private_key}', 'chain_code': f'{chain_code}'}
    return JsonResponse(response)


def generate_address(request, coin):
    now = datetime.now()
    wallet = get_wallet(coin)
    if wallet == None:
        response = {'status': 'error', 'timestamp': f'{now}', 'message': 'coin not supported'}
        return JsonResponse(response)
    count = Master.objects.filter(coin=coin).count()
    if count != 1:
        response = {'status': 'error', 'timestamp': f'{now}', 'message': 'coin master not exist'}
        return JsonResponse(response)
    master = Master.objects.get(coin=coin)
    index = Address.objects.all().count()
    private_key, _ = wallet.derivate_child_private_key(master.private_key, master.chain_code, index)
    address = wallet.generate_address(private_key)
    address_obj = Address(id=index, coin=coin, address=address)
    address_obj.save()
    response = {'status': 'ok', 'timestamp': f'{now}', 'index': f'{index}', 
                'coin': f'{coin}', 'address': f'{address}'}
    return JsonResponse(response)


def list_address(request):
    now = datetime.now()
    addresses = Address.objects.all()
    address_list = [{'index': a.id, 'coin': a.coin, 'address': a.address} for a in addresses]
    response = {'status': 'ok', 'timestamp': f'{now}', 'list_address': address_list}
    return JsonResponse(response)


def retrieve_address(request, id):
    now = datetime.now()
    count = Address.objects.filter(id=id).count()
    if count != 1:
        response = {'status': 'error', 'timestamp': f'{now}', 'message': 'address index not exist'}
        return JsonResponse(response)
    address = Address.objects.get(id=id)
    response = {'status': 'ok', 'timestamp': f'{now}', 'index': id, 
                'coin': address.coin, 'address': address.address}
    return JsonResponse(response)
