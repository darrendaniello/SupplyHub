from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository


class CartService:
    def __init__(self, session: Session):
        self.cart_repository = CartRepository(session)

    def get_cart(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            cart = self.cart_repository.create_cart(user_id)

        items = self.cart_repository.get_items_by_cart(cart.id)

        return {
            "cart": cart,
            "items": items,
        }

    def add_to_cart(
        self,
        user_id: int,
        product_id: int,
        quantity: int,
    ):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            cart = self.cart_repository.create_cart(user_id)

        existing_item = (
            self.cart_repository
            .get_item_by_cart_and_product(
                cart.id,
                product_id,
            )
        )

        if existing_item is not None:
            existing_item.quantity += quantity

            self.cart_repository.update_item(
                existing_item,
                existing_item.quantity,
            )

            return existing_item

        return self.cart_repository.create_item(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        )

    def update_cart_item(
        self,
        user_id: int,
        cart_item_id: int,
        quantity: int,
    ):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            raise ValueError("Cart not found")

        cart_item = self.cart_repository.get_item_by_id(
            cart_item_id
        )

        if cart_item is None:
            raise ValueError("Cart item not found")

        if cart_item.cart_id != cart.id:
            raise ValueError("Cart item does not belong to this user")

        return self.cart_repository.update_item(
            cart_item,
            quantity,
        )

    def remove_from_cart(
        self,
        user_id: int,
        cart_item_id: int,
    ):
        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            raise ValueError("Cart not found")

        cart_item = self.cart_repository.get_item_by_id(
            cart_item_id
        )

        if cart_item is None:
            raise ValueError("Cart item not found")

        if cart_item.cart_id != cart.id:
            raise ValueError("Cart item does not belong to this user")

        self.cart_repository.delete_item(cart_item)

    def clear_cart(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user(user_id)

        if cart is None:
            raise ValueError("Cart not found")

        items = self.cart_repository.get_items_by_cart(
            cart.id
        )

        for item in items:
            self.cart_repository.delete_item(item)