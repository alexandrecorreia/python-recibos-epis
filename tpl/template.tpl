<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Termo de Responsabilidade – EPI</title>
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 10px;
            line-height: 1.2;
            color: #333;
            margin: 10px;
        }

        h1, h2 {
            text-align: center;
        }

        h1 {
            font-size: 18px;
            text-transform: uppercase;
        }

        h2 {
            font-size: 14px;
            margin-top: 25px;
        }

        p {
            text-align: justify;
            margin: 10px 0;
        }

        .box {
            border: 1px solid #ccc;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
            font-size: 9px;
        }

        ul {
            margin-top: 10px;
            padding-left: 20px;
        }

        ul li {
            margin-bottom: 6px;
        }

        .highlight {
            font-weight: bold;
        }

        .employee-name {
            font-size: 13px;
            font-weight: bold;
            margin-top: 20px;
        }

        .signature {
            margin-top: 40px;
        }

        .signature-line {
            margin-top: 60px;
            display: flex;
            justify-content: space-between;
        }

        .signature-line div {
            width: 45%;
            text-align: center;
        }

        .footer {
            margin-top: 15px;
            font-size: 8px;
            color: #666;
            text-align: center;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        table th, table td {
            border: 1px solid #999;
            padding: 8px;
            text-align: left;
        }

        table th {
            background-color: #f2f2f2;
        }
        
        .obligations-container {
            font-size:9px;
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }
        
        .obligation-box {
            width: 50%;
            border: 1px solid #ccc;
            padding: 15px;
            border-radius: 4px;
        }
        
        .obligation-box h2 {
            margin-top: 0;
            text-align: center;
        }
        
    </style>
</head>
<body>

    <h1>Termo de Responsabilidade – EPI</h1>

    <p class="employee-name">
        Colaborador: {{NOME_FUNCIONARIO}}
    </p>

    <div class="box">
        <p>
            <span class="highlight">NR 6.1</span> Para os fins de aplicação desta Norma Regulamentadora – NR, considera-se 
            Equipamento de Proteção Individual – EPI todo dispositivo de uso individual, de fabricação nacional ou estrangeira,
            destinado a proteger a saúde e a integridade física do trabalhador.
        </p>
    </div>

    <div class="obligations-container">
    
        <div class="obligation-box">
            <h2>Obrigações do Empregador</h2>
            <ul>
                <li>Adquirir o tipo adequado de EPI à atividade do colaborador;</li>
                <li>Treinar o colaborador sobre o uso;</li>
                <li>Fornecer ao colaborador somente EPI aprovado pelo MTB e de empresas cadastradas no DNSST/MTb;</li>
                <li>Tornar obrigatório o seu uso e acompanhamento do EPI;</li>
                <li>Substituí-lo, imediatamente, quando danificado, extraviado ou quando houver perda de sua eficácia;</li>
                <li>Comunicar ao MTb qualquer irregularidade no EPI.</li>
            </ul>
        </div>
    
        <div class="obligation-box">
            <h2>Obrigações dos Colaboradores</h2>
            <ul>
                <li>Usá-lo apenas para a finalidade a que se destina;</li>
                <li>Responsabilizar-se por sua guarda e conservação;</li>
                <li>Comunicar ao empregador qualquer alteração que o torne impróprio para o uso.</li>
            </ul>
        </div>
    
    </div>


    <h2>Termo de Responsabilidade</h2>
    <p>
        Recebi, de <strong>{{NOME_DA_EMPRESA}}</strong>, os EPI’s adequados abaixo, os quais desde já me comprometo a sempre usar
        na execução de minhas tarefas, zelando pela sua perfeita guarda e conservação, uso e funcionamento, de acordo com as
        orientações e treinamentos recebidos pela CIPA e/ou SESMT, assumindo também o compromisso de devolvê-los quando solicitado
        ou por ocasião de rescisão de meu contrato de trabalho.Estou ciente e de pleno acordo que o não cumprimento das condições 
        estabelecidas acarretará, além da aplicação de penas disciplinares, inclusive rescisão do meu contrato laboral, outras sanções 
        previstas em lei, em especial as constantes na NR 06, Portaria nº 3.214 de 08/06/1997, do Ministério do Trabalho.
    </p>

    <p>
        No caso de perda, dano, extravio ou avaria, por negligência minha, dos equipamentos de proteção,
        <strong>RESPONDEREI POR AÇÃO INDISCIPLINAR</strong>.
    </p>

    <h2>Ato Faltoso</h2>
    <p>
        “Constitui-se ato faltoso do colaborador a recusa injustificada do uso e/ou conservação dos EPI’s – Equipamento de Proteção
        Individual fornecidos pela empresa.” (Conforme previsto na legislação vigente, artigo 482 da CLT).
    </p>

    <!-- Tabela dinâmica de itens de EPI -->
    {{TABELA_DE_ITENS}}

    <div class="signature">
        E para constar, assino a presente para produção dos efeitos legais.
        <br>
        <br>
        <br>
        
        {{DATA_HOJE}} __________________________________________ <br>
        <strong>Assinatura do Colaborador - {{NOME_FUNCIONARIO}}</strong>
    </div>

    <div class="footer">
        Documento gerado eletronicamente para fins legais e administrativos.
    </div>

</body>
</html>
