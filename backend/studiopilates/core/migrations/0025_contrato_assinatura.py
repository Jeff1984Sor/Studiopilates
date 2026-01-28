from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0024_profissional_email_celular"),
    ]

    operations = [
        migrations.AddField(
            model_name="contrato",
            name="status",
            field=models.CharField(
                choices=[("NAO_ASSINADO", "Nao assinado"), ("ASSINADO", "Contrato assinado")],
                default="NAO_ASSINADO",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contrato",
            name="assinado_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contrato",
            name="assinatura_nome",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="contrato",
            name="assinatura_documento",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="contrato",
            name="assinatura_ip",
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contrato",
            name="assinatura_imagem",
            field=models.ImageField(blank=True, null=True, upload_to="assinaturas"),
        ),
    ]
