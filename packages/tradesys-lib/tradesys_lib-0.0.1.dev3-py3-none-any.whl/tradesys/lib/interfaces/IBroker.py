from abc import ABC, abstractmethod
from typing import Union, List, Tuple
import difflib
from ..types import Symbol, Commission, User, AccountBalance, TimeStamp, TradeTransaction, Credentials


class IBroker(ABC):
    client = None
    authenticated = False
    # TODO Implement dummy streaming client.
    stream = None

    @abstractmethod
    def connect(self, user: Union[str, int] = "", password: str = None) -> bool:
        pass

    @abstractmethod
    def connect_with_credentials(self, credentials: Credentials) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_symbol(self, symbol: Union[str, Symbol]) -> Symbol:
        pass

    def search_symbol(self, symbol: str) -> Union[None, Symbol]:
        all_symbols = self.get_available_symbols()
        all_symbols_str = [sym.symbol for sym in all_symbols]
        matches = difflib.get_close_matches(symbol, all_symbols_str, 3)
        if len(matches) == 1:
            return self.get_symbol(str(matches[0]))
        else:
            print(f"Closest matches: {matches}")

        return None

    @abstractmethod
    def get_available_symbols(self) -> List[Symbol]:
        pass

    @abstractmethod
    def get_commission(self, volume: float, symbol: Union[str, Symbol]) -> Commission:
        pass

    @abstractmethod
    def get_current_user_data(self) -> User:
        pass

    @abstractmethod
    def get_account_balance(self) -> AccountBalance:
        pass

    @abstractmethod
    def get_server_time(self) -> TimeStamp:
        # Returns unix timestamp of server time
        pass

    @abstractmethod
    def get_version(self) -> str:
        pass

    @abstractmethod
    def connection_status(self) -> bool:
        pass

    @abstractmethod
    def check_transaction_status(self, transaction: TradeTransaction) -> bool:
        pass

    @abstractmethod
    def open_buy_position(self, transaction: TradeTransaction) -> Tuple[bool, TradeTransaction]:
        pass


class IStreamingBroker(IBroker, ABC):
    pass
