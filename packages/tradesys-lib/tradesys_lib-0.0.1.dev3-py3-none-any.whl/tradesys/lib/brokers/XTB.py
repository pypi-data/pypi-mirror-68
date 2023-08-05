from typing import Tuple, Union, List
from ..connectors.xAPIConnector import APIClient
from ..interfaces.IBroker import IBroker
from ..types import TradeTransaction, TimeStamp, AccountBalance, User, Symbol, Commission, Credentials


class XTBClient(IBroker):

    def __init__(self):
        self.client = APIClient()
        self.streamSessionId = None

    def connect(self, user: Union[int, str] = None, password: str = None) -> bool:
        login_response = self.client.commandExecute('login', dict(userId=user, password=password))
        if login_response['status'] is False:
            print(
                f"Authentication error. Error code: {login_response['errorCode']}\nError message: {login_response['errorDescr']}")
            return self.authenticated

        self.streamSessionId = login_response['streamSessionId']
        self.authenticated = login_response['status']
        return self.authenticated

    def connect_with_credentials(self, credentials: Credentials) -> bool:
        if credentials.is_token:
            raise TypeError("XTB cannot accept a token credentials.")
        return self.connect(credentials.username, credentials.password)

    def disconnect(self) -> None:
        self.client.commandExecute('logout')
        self.client.disconnect()

    def get_symbol(self, symbol: Union[str, Symbol]) -> Symbol:
        if type(symbol) == str:
            symbol_command = self.client.commandExecute("getSymbol", dict(symbol=symbol))
        elif type(symbol) == Symbol:
            symbol_command = self.client.commandExecute("getSymbol", dict(symbol=symbol.symbol))
        else:
            raise TypeError("Passed parameter is not of type Symbol or str.")

        # Check status
        assert symbol_command['status'] is True

        # Return result
        symbol = symbol_command['returnData']
        return Symbol(symbol=symbol['symbol'],
                      ask=symbol['ask'],
                      bid=symbol['bid'],
                      category=symbol['categoryName'],
                      contract_size=symbol['contractSize'],
                      currency=symbol['currency'],
                      currency_pair=symbol['currencyPair'],
                      currency_profit=symbol['currencyProfit'],
                      description=symbol['description'],
                      expiration=symbol['expiration'],
                      high=symbol['high'],
                      initial_margin=symbol['initialMargin'],
                      leverage=symbol['leverage'],
                      long_only=symbol['longOnly'],
                      min_lot=symbol['lotMin'],
                      max_lot=symbol['lotMax'],
                      lot_step=symbol['lotStep'],
                      low=symbol['low'],
                      pip_precision=symbol['pipsPrecision'],
                      price_precision=symbol['precision'],
                      shortable=symbol['shortSelling'],
                      time=TimeStamp(symbol['time'], unix=True, milliseconds=True)
                      )

    def get_available_symbols(self) -> List[Symbol]:
        response = self.client.commandExecute('getAllSymbols')
        symbols = response['returnData']
        available_symbols = []
        for symbol in symbols:
            s = Symbol(symbol=symbol['symbol'],
                       ask=symbol['ask'],
                       bid=symbol['bid'],
                       category=symbol['categoryName'],
                       contract_size=symbol['contractSize'],
                       currency=symbol['currency'],
                       currency_pair=symbol['currencyPair'],
                       currency_profit=symbol['currencyProfit'],
                       description=symbol['description'],
                       expiration=symbol['expiration'],
                       high=symbol['high'],
                       initial_margin=symbol['initialMargin'],
                       leverage=symbol['leverage'],
                       long_only=symbol['longOnly'],
                       min_lot=symbol['lotMin'],
                       max_lot=symbol['lotMax'],
                       lot_step=symbol['lotStep'],
                       low=symbol['low'],
                       pip_precision=symbol['pipsPrecision'],
                       price_precision=symbol['precision'],
                       shortable=symbol['shortSelling'],
                       time=TimeStamp(symbol['time'], unix=True, milliseconds=True)
                       )
            available_symbols.append(s)

        return available_symbols

    def get_commission(self, volume: float, symbol: Union[str, Symbol]) -> Commission:
        if type(symbol) == str:
            res = self.client.commandExecute("getCommissionDef", dict(symbol=symbol, volume=volume))
        elif type(symbol) == Symbol:
            res = self.client.commandExecute("getCommissionDef", dict(symbol=symbol.symbol, volume=volume))
        else:
            raise TypeError("Passed parameter is not of type Symbol or str.")

        assert res['status'] is True

        commission = res['returnData']

        return Commission(commission=commission['commission'],
                          exchange_rate=commission['rateOfExchange'])

    def get_current_user_data(self) -> User:
        raise NotImplementedError("This feature is still under development.")

    def get_account_balance(self) -> AccountBalance:
        res = self.client.commandExecute("getMarginLevel")
        assert res['status'] is True
        data = res['returnData']
        return AccountBalance(
            balance=data["balance"],
            credit=data['credit'],
            currency=data['currency'],
            equity=data['equity'],
            margin=data['margin'],
            free_margin=data['margin_free']
        )

    def get_server_time(self) -> TimeStamp:
        res = self.client.commandExecute("getServerTime")
        assert res['status'] is True
        data = res['returnData']
        return TimeStamp(time_value=data['time'], unix=True, milliseconds=True)

    def get_version(self) -> str:
        res = self.client.commandExecute("getVersion")
        assert res['status'] is True

        return res['returnData']['version']

    def connection_status(self) -> bool:
        res = self.client.commandExecute("ping")
        try:
            # Leveraging the fact that None type is falsy.
            if res['status']:
                return True
        except:
            # If for some reason it fails (it shouldn't) just ignore and return default False
            pass

        return False

    def check_transaction_status(self, transaction: TradeTransaction) -> bool:
        raise NotImplementedError("This feature is still under development.")

    def open_buy_position(self, transaction: TradeTransaction) -> Tuple[bool, TradeTransaction]:
        raise NotImplementedError("This feature is still under development.")
