from typing import Dict, List, Optional

from django.db.models import Max, Min, Q, QuerySet
from ninja import Router

from example.models import Coin, CoinMarketData
from example.schema import CoinMarketDataListSchema, CoinMarketDataSchema, CoinSchema

router = Router()


@router.get("/", response=List[CoinSchema])
def coins_list(request):
    queryset = Coin.objects.all()
    return list(queryset)


@router.get("/detail/{symbol}", response=List[CoinMarketDataListSchema])
def coin_detail(request, symbol: str):
    queryset = CoinMarketData.objects.filter(coin__symbol=symbol)
    return list(queryset)


@router.get(
    "/search-transaction/{symbol}/{year}-{month}-{day}",
    response=List[CoinMarketDataSchema],
)
def search_transaction(request, symbol: str, year: str, month: str, day: str):
    queryset = CoinMarketData.objects.filter(
        coin__symbol=symbol, date__year=year, date__month=month, date__day=day
    )
    return list(queryset)


@router.get(
    "/best-transaction/{start_date}/{end_date}", response=List[CoinMarketDataSchema]
)
def search_transaction(request, start_date: str, end_date: str):
    base_queryset = CoinMarketData.objects.filter(date__range=[start_date, end_date])
    results = get_results(base_queryset)

    return results


def get_max_diff_item(queryset: QuerySet, excluded_items: List) -> Optional[Dict]:
    max_diff_item = None
    max_diff = 0
    for item in queryset:
        if item["diff"] > max_diff and item not in excluded_items:
            max_diff_item = item
            max_diff = item["diff"]
    return max_diff_item


def get_transactions(base_queryset: QuerySet, max_diff_item: Dict) -> Optional[List]:
    try:
        low_transaction = (
            base_queryset.filter(coin_id=max_diff_item["coin"])
            .filter(low=max_diff_item["min_low"])
            .first()
        )
        high_transaction = (
            base_queryset.filter(
                coin_id=max_diff_item["coin"], date__gt=low_transaction.date
            )
            .filter(high=max_diff_item["max_high"])
            .first()
        )
        return [low_transaction, high_transaction]
    except Exception:
        return None


def get_results(base_queryset: QuerySet) -> Optional[List]:
    results = None
    iterations = 0
    queryset = base_queryset.values("coin").annotate(
        min_low=Min("low"), max_high=Max("high"), diff=Max("high") - Min("low")
    )
    max_iterations = queryset.count()
    while results is None and iterations < max_iterations:
        max_diff_item = get_max_diff_item(queryset, [])
        results = get_transactions(base_queryset, max_diff_item)
        iterations += 1

    return results
