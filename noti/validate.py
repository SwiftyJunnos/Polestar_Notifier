
def validate_stock(
    stock: int
) -> bool:
    if stock == 0:
        return False
    elif stock > 0:
        return True