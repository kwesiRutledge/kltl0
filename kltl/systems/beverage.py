
from kltl0.src.systems import TransitionSystem

def get_beverage_vending_machine():
    """
    Returns a beverage vending machine transition system.
    :return:
    """
    # Constants
    S = ["start", "pay", "select", "dispense", "end"]
    Act = ["coin", "select", "dispense"]
    AP = ["paid", "selected", "dispensed"]
    I = ["start"]
    transitions = [
        ("start", "coin", "pay"),
        ("pay", "select", "select"),
        ("select", "dispense", "dispense"),
        ("dispense", "coin", "pay"),
        ("dispense", "select", "select"),
        ("dispense", "dispense", "dispense"),
        ("pay", "coin", "pay"),
        ("pay", "select", "select"),
        ("pay", "dispense", "dispense"),
        ("select", "coin", "select"),
        ("select", "select", "select"),
        ("select", "dispense", "dispense"),
    ]
    labels = [
        ("pay", "paid"),
        ("select", "selected"),
        ("dispense", "dispensed"),
    ]

    # Create the transition system
    ts = TransitionSystem(S, Act, AP, I, transitions, labels)

    return ts