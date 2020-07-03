-- create rental entry
Set @inventoryID = (SELECT inventory_id FROM inventory order by rand() limit 1);
Set @customerID = (SELECT customer_id FROM customer order by rand() limit 1);
Set @createDate = (select from_unixtime(unix_timestamp('2020-1-1') + floor(rand() * (unix_timestamp('2020-6-3') - unix_timestamp('2020-1-1') + 1))));
INSERT into rental(rental_date, inventory_id, customer_id, return_date, staff_id, last_update, created_date, order_confirmed_date, order_rejected_date, return_inspected_date)
SELECT	NULL,
        @inventoryID,
        @customerID,
        NULL,
		(SELECT staff_id FROM staff, (SELECT store_id FROM inventory where inventory.inventory_id=@inventoryID) as fitStoreId Where fitStoreId.store_id=staff.store_id order by rand()  limit 1),
        @createDate,
		@createDate,
        NULL,
        NULL,
        NULL;
        
-- create inventory entry
INSERT into inventory(equipment_id, store_id,last_update)
SELECT	(SELECT equipment_id FROM equipment order by rand() limit 1),
        (SELECT store_id FROM store order by rand() limit 1),
		(select from_unixtime(unix_timestamp('2019-12-20') + floor(rand() * (unix_timestamp('2019-12-31') - unix_timestamp('2019-12-20') + 1))));
     
-- update stuff
UPDATE staff 
SET 
    store_id = 2
WHERE
    staff_id = 20;
    
-- reset auto increment
alter table rental auto_increment = 1