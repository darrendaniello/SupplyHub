from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart, CartItem


class CartRepository:
    def __init__(self, session: Session):
        self.session = session

    # =========================
    # Cart
    # =========================

    def get_cart_by_id(self, cart_id: int):
        stmt = (
            select(Cart)
            .where(Cart.id == cart_id)
        )

        return self.session.scalar(stmt)

    def get_cart_by_user(self, user_id: int):
        stmt = (
            select(Cart)
            .where(Cart.user_id == user_id)
        )

        return self.session.scalar(stmt)

    def create_cart(self, user_id: int):
        cart = Cart(
            user_id=user_id
        )

        self.session.add(cart)
        self.session.flush()

        return cart

    def delete_cart(self, cart: Cart):
        self.session.delete(cart)
        self.session.flush()

    # =========================
    # Cart Item
    # =========================

    def get_item_by_id(self, cart_item_id: int):
        stmt = (
            select(CartItem)
            .where(CartItem.id == cart_item_id)
        )

        return self.session.scalar(stmt)

    def get_items_by_cart(self, cart_id: int):
        stmt = (
            select(CartItem)
            .options(joinedload(CartItem.product))
            .where(CartItem.cart_id == cart_id)
            .order_by(CartItem.id)
        )

        return self.session.scalars(stmt).all()

    def get_item_by_cart_and_product(
        self,
        cart_id: int,
        product_id: int,
    ):
        stmt = (
            select(CartItem)
            .where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
        )

        return self.session.scalar(stmt)

    def create_item(
        self,
        cart_id: int,
        product_id: int,
        quantity: int,
    ):
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        )

        self.session.add(cart_item)
        self.session.flush()

        return cart_item

    def update_item(
        self,
        cart_item: CartItem,
        quantity: int,
    ):
        cart_item.quantity = quantity

        self.session.flush()

        return cart_item

    def delete_item(self, cart_item: CartItem):
        self.session.delete(cart_item)
        self.session.flush()