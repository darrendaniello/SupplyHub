from app.database import SessionLocal
from app.repositories.inventory_repository import InventoryRepository


def test_get_inventory_by_id():
    with SessionLocal() as session:
        repository = InventoryRepository(session)

        inventory = repository.get_by_id(1)

        print(
            f"Inventory ID: {inventory.id}"
        )
        print(
            f"Product ID: {inventory.product_id}"
        )
        print(
            f"Stock: {inventory.stock_quantity}"
        )
        print(
            f"Reserved: {inventory.reserved_quantity}"
        )


def test_get_inventory_by_product():
    with SessionLocal() as session:
        repository = InventoryRepository(session)

        inventory = repository.get_by_product(1)

        print(
            f"Inventory ID: {inventory.id}"
        )
        print(
            f"Product ID: {inventory.product_id}"
        )


def test_get_available_quantity():
    with SessionLocal() as session:
        repository = InventoryRepository(session)

        available = repository.get_available_quantity(1)

        print(
            f"Available quantity: {available}"
        )


def test_create_inventory():
    with SessionLocal() as session:
        repository = InventoryRepository(session)

        inventory = repository.create(
            product_id=1,
            stock_quantity=100,
            reserved_quantity=10,
        )

        session.commit()

        print(
            f"Created inventory ID: {inventory.id}"
        )


def test_update_inventory():
    with SessionLocal() as session:
        repository = InventoryRepository(session)

        inventory = repository.get_by_product(1)

        inventory = repository.update(
            inventory,
            stock_quantity=90,
            reserved_quantity=15,
        )

        session.commit()

        print(
            f"Updated stock: {inventory.stock_quantity}"
        )
        print(
            f"Updated reserved: {inventory.reserved_quantity}"
        )


def test_delete_inventory():
    with SessionLocal() as session:
        repository = InventoryRepository(session)

        inventory = repository.get_by_product(1)

        repository.delete(inventory)

        session.commit()

        print("Inventory deleted")


if __name__ == "__main__":
    test_get_inventory_by_id()
    test_get_inventory_by_product()
    test_get_available_quantity()
    # test_create_inventory()
    # test_update_inventory()
    # test_delete_inventory()