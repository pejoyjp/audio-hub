from .unit_test import test_create_user, test_login

# Run unit tests
try:
    test_create_user()
    print("All test of Create User have run successfully")
except:
    raise AssertionError("Create user tests didn't pass")

try:
    test_login()
    print("All test of Log in have run successfully")
except:
    raise AssertionError("Log in tests didn't pass")
