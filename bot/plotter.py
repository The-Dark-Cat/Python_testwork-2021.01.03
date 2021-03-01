import matplotlib.pyplot as plt
import os


async def plot(x, y, currency):
    await checkdir('filedir')
    path = f'filedir/{currency}-{x[0]}.png'
    plt.grid()
    plt.ylabel(f"{currency} for USD", fontsize=10)
    plt.xlabel("date", fontsize=10)
    plt.tick_params(
        labelrotation=45
    )
    plt.autoscale()
    plt.plot(x, y)
    plt.savefig(fname=path)
    # plt.show()
    return path


async def checkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
