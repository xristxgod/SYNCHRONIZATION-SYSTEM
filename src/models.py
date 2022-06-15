from tortoise import fields, models


class UserModel(models.Model):
    id = fields.BigIntField(pk=True, unique=True)
    username = fields.CharField(max_length=255, null=True, default=None)

    wallet: fields.ReverseRelation["WalletModel"]

    class Meta:
        allow_cycles = True


class WalletModel(models.Model):
    address = fields.CharField(max_length=255, pk=True, unique=True)
    private_key = fields.CharField(max_length=255, unique=True)
    balance = fields.DecimalField(max_digits=18, decimal_places=8, default=0)
    user_id = fields.OneToOneField('models.UserModel', related_name='wallet', on_delete=fields.CASCADE)


class AccountModel:
    id = fields.IntField(pk=True, unique=True)
    api_name = fields.CharField(max_length=255, unique=True)
    api_key = fields.CharField(max_length=255, unique=True)
    secret_key = fields.CharField(max_length=255, unique=True)
    user_id = fields.ForeignKeyField('models.UserModel', related_name="user_id", on_delete=fields.CASCADE)


class OrderModel:
    pass
