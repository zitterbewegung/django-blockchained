# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from solc import compile_source
from web3 import Web3, HTTPProvider,TestRPCProvider
from web3.contract import ConciseContract

#from .models import Contract
#from .forms import ContractForm

########################################################################
# def list(request):                                                   #
#     # Handle file upload                                             #
#     if request.method == 'POST':                                     #
#         form = ContractForm(request.POST, request.FILES)             #
#         if form.is_valid():                                          #
#             newdoc = Contract(docfile = request.FILES['docfile'])    #
#             newdoc.save()                                            #
#                                                                      #
#             # Redirect to the document list after POST               #
#             return HttpResponseRedirect(reverse('myapp.views.list')) #
#     else:                                                            #
#         form = DocumentForm() # A empty, unbound form                #
#                                                                      #
#     # Load documents for the list page                               #
#     documents = Document.objects.all()                               #
#                                                                      #
#     # Render list page with the documents and the form               #
#     return render_to_response(                                       #
#         'myapp/list.html',                                           #
#         {'documents': documents, 'form': form},                      #
#         context_instance=RequestContext(request)                     #
#     )                                                                #
########################################################################

# Create your views here.

w3 = Web3(TestRPCProvider())


def index(request):

    block = w3.eth.getBlock('latest')


    return HttpResponse("Hello, world. The latest block is:" + str(block.number))

def calculate_pi(request):
    # the candidates we're allowing people to vote for
    # note that each name is being encoded to bytes because our contract 
    # type is bytes32[]
    VOTING_CANDIDATES = ['Rama'.encode(), 'Nick'.encode(), 'Jose'.encode()]

    # open a connection to the testrpc
    http_provider = HTTPProvider('http://localhost:8545')
    eth_provider = Web3(http_provider).eth
    # we'll use one of our default accounts to deploy from. every write to the chain requires a
    # payment of ethereum called "gas". if we were running an actual test ethereum node locally,
    # then we'd have to go on the test net and get some free ethereum to play with. that is beyond
    # the scope of this tutorial so we're using a mini local node that has unlimited ethereum and
    # the only chain we're using is our own local one
    default_account = eth_provider.accounts[0]
    # every time we write to the chain it's considered a "transaction". every time a transaction
    # is made we need to send with it at a minimum the info of the account that is paying for the gas
    transaction_details = {
        'from': default_account,
    }
    # if not app.config.get('CONTRACT_ADDRESS'):
    # load our Solidity code into an object
    with open('/Users/r2q2/Desktop/work/django-ethereum-starter/django_ethereum_starter/django-blockchained/vorpal/solidity/Division.sol') as file:
        source_code = file.readlines()
    # compile the contract
    compiled_code = compile_source(''.join(source_code))

    # contract name so we keep our code DRY
    contract_name = 'Divide'

    # lets make the code a bit more readable by storing the values in variables
    contract_bytecode = compiled_code[f'<stdin>:{contract_name}']['bin']
    contract_abi = compiled_code[f'<stdin>:{contract_name}']['abi']
    # the contract abi is important. it's a json representation of our smart contract. this
    # allows other APIs like JavaScript to understand how to interact with our contract without
    # reverse engineering our compiled code

    # create a contract factory. we'll use this to deploy any number of
    # instances of the contract to the chain
    contract_factory = eth_provider.contract(
        abi=contract_abi,
        bytecode=contract_bytecode,
    )
    # here we deploy the smart contract
    # two things are passed into the deploy function:
    #   1. info about how we want to deploy to the chain
    #   2. the arguments to pass the smart contract constructor
    # the deploy() function returns a transaction hash. this is like the id of the
    # transaction that initially put the contract on the chain
    transaction_hash = contract_factory.deploy(
        # the bare minimum info we give about the deployment is which ethereum account
        # is paying the gas to put the contract on the chain
        transaction=transaction_details,
        # here was pass in a list of smart contract constructor arguments
        # our contract constructor takes only one argument, a list of candidate names
        args=[VOTING_CANDIDATES],
    )

    # if we want our frontend to use our deployed contract as it's backend, the frontend
    # needs to know the address where the contract is located. we use the id of the transaction
    # to get the full transaction details, then we get the contract address from there
    transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
    contract_address = transaction_receipt['contractAddress']

    contract_instance = eth_provider.contract(
        abi=contract_abi,
        address=contract_address,
        # when a contract instance is converted to python, way call the native solidity
        # functions like: contract_instance.call().someFunctionHere()
        # the .call() notation becomes repetitive so we can pass in ConciseContract as our
        # parent class, allowing us to make calls like: contract_instance.someFunctionHere()
        ContractFactoryClass=ConciseContract,
    )
    pi_in_decimal = contract_instance.percent(22,7,10)
    return HttpResponse("The value of pi returned is %i." % pi_in_decimal)
##################################################################################
# def detail(request, block_id):                                                 #
#                                                                                #
#     block = w3.eth.getBlock(reqblock_id)                                       #
#     return HttpResponse("You're looking at block %s." % str(block.number))     #
#                                                                                #
#                                                                                #
# def compiled_voting_contract(request):                                         #
#     contract_source_code = '''                                                 #
#     pragma solidity ^0.4.0;                                                    #
#                                                                                #
#     contract Greeter {                                                         #
#         string public greeting;                                                #
#                                                                                #
#         function Greeter() {                                                   #
#             greeting = 'Hello';                                                #
#         }                                                                      #
#                                                                                #
#         function setGreeting(string _greeting) public {                        #
#             greeting = _greeting;                                              #
#         }                                                                      #
#                                                                                #
#         function greet() constant returns (string) {                           #
#             return greeting;                                                   #
#         }                                                                      #
#     }                                                                          #
#     '''                                                                        #
#                                                                                #
#     compiled_sol = compile_source(contract_source_code) # Compiled source code #
#     #contract_interface = compiled_sol['<stdin>:Greeter']                      #
#                                                                                #
#                                                                                #
#                                                                                #
# def contractor(request):                                                       #
#                                                                                #
#     #template = loader.get_template('vorpal/MyToken.sol')                      #
#     #context = {}                                                              #
#                                                                                #
#     return render(request, 'vorpal/solidity/MyToken.sol', {                    #
#         'foo': 'bar',                                                          #
#     }, content_type='application/xhtml+xml')                                   #
##################################################################################
