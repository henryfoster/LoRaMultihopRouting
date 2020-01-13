from models.Route import Route

route1 = Route("0014", 1, "0014")
route3 = Route("0014", 1, "0014")
route2 = Route("0016", 2, "0014")

print(route1)
print(route2)
route2.hop_count += 1
print(route2)

print(route2 == route1)
print(route1 == route3)