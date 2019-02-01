import matplotlib.pyplot as plt


def draw(customers, depots, paths=None, fill_stations=None):
    for customer in customers:
        plt.scatter(customer.x, customer.y, alpha=0.5, c='C1', s=10)
    for depot in depots:
        plt.scatter(depot.x, depot.y, alpha=0.5, c='C5', marker='s', s=30)

    if fill_stations is not None:
        for station in fill_stations:
            plt.scatter(station.x, station.y, alpha=0.5, c='C4', marker='p', s=30)

    if paths is not None:
        for x1, y1, x2, y2, vehicle_i in paths:
            plt.plot([x1, x2], [y1, y2], color=('C'+str(vehicle_i)), linewidth=1)
