def format_individual_residences(residences):
    return [
            {
                "domicilio_id": r.DomicilioIndividuo.domicilio_id,
                "data_residencia": r.DomicilioIndividuo.data_residencia.isoformat() if r.DomicilioIndividuo.data_residencia else None,
                "mudou": r.DomicilioIndividuo.mudou,
                "renda_familia_salario_minimos": float(
                    r.DomicilioIndividuo.renda_familia_salario_minimos) if r.DomicilioIndividuo.renda_familia_salario_minimos else None,
                "n_membros_familia": r.DomicilioIndividuo.n_membros_familia,
                "responsavel": r.DomicilioIndividuo.responsavel,
                "endereco_completo": f"{r.tipo_logradouro} {r.nome_logradouro}, {r.numero}" + (
                    f", {r.complemento}" if r.complemento else ""),
                "bairro": r.bairro,
                "municipio": r.municipio,
                "uf": r.uf,
                "cep": r.cep
            }
            for r in residences
        ]
