from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3, TestRPCProvider
from django.template import loader

# Create your views here.

w3 = Web3(TestRPCProvider())


def index(request):

    block = w3.eth.getBlock('latest')

    return HttpResponse("Hello, world. The latest block is:" + str(block.number))


def detail(request, block_id):
   
    block = w3.eth.getBlock(block_id)
    return HttpResponse("You're looking at block %s." % str(block.number))

def contractor(request):
    
    #template = loader.get_template('vorpal/MyToken.sol')
    #context = {}

    return render(request, 'vorpal/solidity/MyToken.sol', {
        'foo': 'bar',
    }, content_type='application/xhtml+xml')

