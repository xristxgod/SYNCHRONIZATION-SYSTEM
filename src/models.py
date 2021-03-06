from tortoise import fields, models


# <<<==========================================>>> Base models <<<===================================================>>>


class UserModel(models.Model):
    id = fields.BigIntField(pk=True, unique=True)
    username = fields.CharField(max_length=255, null=True, default=None)
    is_admin = fields.BooleanField(default=False)

    wallet: fields.ReverseRelation["WalletModel"]

    class Meta:
        allow_cycles = True


class WalletModel(models.Model):
    address = fields.CharField(max_length=255, pk=True, unique=True)
    private_key = fields.CharField(max_length=255, unique=True)
    balance = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    user_id = fields.OneToOneField('models.UserModel', related_name='wallet', on_delete=fields.CASCADE)


class AccountModel(models.Model):
    api_name = fields.CharField(max_length=255, pk=True, unique=True)
    api_key = fields.CharField(max_length=255, unique=True)
    secret_key = fields.CharField(max_length=255, unique=True)
    totalWalletBalance = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    totalUnrealizedProfit = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    totalMarginBalance = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    availableBalance = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    maxWithdrawAmount = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


# <<<==========================================>>> Binance models <<<================================================>>>


class OrderModel(models.Model):
    id = fields.IntField(pk=True, unique=True)
    origQty = fields.FloatField()
    price = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    side = fields.CharField(max_length=32)
    positionSide = fields.CharField(max_length=32)
    status = fields.CharField(max_length=32)
    symbol = fields.CharField(max_length=32)
    time = fields.IntField()
    type = fields.CharField(max_length=32)
    api_name = fields.ForeignKeyField('models.AccountModel', related_name="api_name", on_delete=fields.CASCADE)
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


class IncomeModel(models.Model):
    id = fields.IntField(pk=True, unique=True)
    tranId = fields.IntField()
    symbol = fields.CharField(max_length=32)
    incomeType = fields.CharField(max_length=255)
    income = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    asset = fields.CharField(max_length=255)
    info = fields.CharField(max_length=255)
    time = fields.IntField()
    tradeId = fields.IntField()
    api_name = fields.ForeignKeyField('models.AccountModel', related_name="api_name", on_delete=fields.CASCADE)
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


class PositionModel(models.Model):
    id = fields.IntField(pk=True, unique=True)
    symbol = fields.CharField(max_length=32)
    unrealizedProfit = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    leverage = fields.IntField()
    liquidationPrice = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    entryPrice = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    positionSide = fields.CharField(max_length=32)
    positionAmt = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    api_name = fields.ForeignKeyField('models.AccountModel', related_name="api_name", on_delete=fields.CASCADE)
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


# <<<==========================================>>> Transaction models <<<============================================>>>


class TransactionModel(models.Model):
    pass
