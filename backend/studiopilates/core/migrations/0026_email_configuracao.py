from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0025_contrato_assinatura"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailConfiguracao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cdEmail", models.IntegerField(db_index=True, unique=True)),
                ("host", models.CharField(max_length=120)),
                ("porta", models.IntegerField(default=587)),
                ("usuario", models.CharField(max_length=150)),
                ("senha", models.CharField(max_length=150)),
                ("use_tls", models.BooleanField(default=True)),
                ("remetente", models.EmailField(max_length=254)),
                ("ativo", models.BooleanField(default=True)),
                ("dtCadastro", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
