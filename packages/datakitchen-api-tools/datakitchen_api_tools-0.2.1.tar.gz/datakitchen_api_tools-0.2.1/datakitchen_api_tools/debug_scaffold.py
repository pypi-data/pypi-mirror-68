import DKConnection

conn = DKConnection.DKConnection('cloud.datakitchen.io', 'armand+hm@datakitchen.io', '%Gun8D9M' )
results = conn.safeCreateOrder('armand_gpc', 'car_t', 'variation1', test_level="Warning")
print(results)
