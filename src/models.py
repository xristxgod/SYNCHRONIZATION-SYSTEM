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
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


# <<<==========================================>>> Order models <<<==================================================>>>


class OrderModel(models.Model):
    id = fields.IntField(pk=True, unique=True)
    orig_qty = fields.FloatField()
    price = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    side = fields.CharField(max_length=32)
    position_side = fields.CharField(max_length=32)
    status = fields.CharField(max_length=32)
    symbol = fields.CharField(max_length=32)
    time = fields.IntField()
    api_name = fields.ForeignKeyField('models.AccountModel', related_name="api_name", on_delete=fields.CASCADE)
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


# <<<==========================================>>> Transaction models <<<============================================>>>


class TransactionModel(models.Model):
    pass
