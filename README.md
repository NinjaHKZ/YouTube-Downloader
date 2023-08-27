# <p style='color: red;'>< 🥤 PYTHON - YOUTUBE DOWNLOADER 2.0 🥤 ></p>
<p>
  <img src="https://github.com/NinjaHKZ/YouTube-Downloader/assets/100825381/0c008def-2c64-4f65-94b9-1dd81abbfd4d">
  <em><a href='https://mundowallpaperlp.blogspot.com/2016/03/anime-paisaje.html'>Ache mais Imagens como essa clicando aqui!</a></em>
</p>

## Agradecimentos
 ✅ Primeiramente gostaria agradecer a todos que decidiram confiar, usar e que pensam em colaborar com o projeto, muito obrigado a todos, são vocês que motivam a nossa comunidade a evoluir ❤️.
 
- ❓ **O que há de novo nessa versão?** Esse é a versão 2.0 do antigo baixador, dessa vez foi introduzido correções de bugs que existiam na versão anterior, suporte para downloads de videos, músicas e o melhor, agora com suporte de download assíncrono, também implementamos o suporte para arquivos de texto com URLs/IDs para downloads em massa e facilitar a vida do usuário.

- ❗ **Achei um erro, o que posso fazer?** Caso encontre algum erro durante o uso, você pode contribuir com nosso projeto corrigindo o erro e fazendo pull requests ou simplesmente abrindo uma issue para assim então corrigirmos o erro o mais rápido possível, também poderá entrar em contato com o desenvolvedor para realizar o report pelo próprio software!

###### 🐍 Made with Python Power 🎖 Coded By NinjaHKZ [ Dev. Marcos H. Albach ] 🍝 [NinjaHKZ Apoia-se](https://apoia.se/ninja_hkz)

## 🛠️INSTRUÇÃO DE USO🛠️

⭐Nessa parte iremos abordar a utilização e funcionalidades do programa, comandos, argumentos e outros pontos a respeito de sua utilização!

> ![image](https://github.com/NinjaHKZ/YouTube-Downloader/assets/100825381/98cda3af-8caa-4b17-9f09-5320bd95d2c6) 
> ![image](https://github.com/NinjaHKZ/YouTube-Downloader/assets/100825381/53a5b3bb-1bc5-4d7f-8d23-3b7c6ebab65f)  

### Overview Básico:
```console
python .\main.py -u jKvcHQZP540 -m video -r 360, 720, 1080 
```

| ARGUMENTO | ABREVIAÇÃO | TIPO | FUNÇÃO |
|-----------|------------|------|--------|
| **--url**  | _-u_ | string/arquivo | passa url, id ou um arquivo de texto com as urls para download |
| **--mediatype** | _-m_ | string | passa o tipo de media que deseja, sendo video ou audio |
| **--resolution** | _-r_ | list | define uma lista de resoluções para baixar |
| **--path** | _-p_ | string | define a pasta onde os downloads devem ser inseridos |
| **--url_per_tasks** | _-utasks_ | int | define o tanto de downloads por tasks(1 para baixar todos ao mesmo tempo) | 


### Baixando Links Salvos Em Um Arquivo:
✨ Para baixar uma lista de urls salvos em um arquivo é simples, basta inserir as url em um arquivo de texto e depois de salvo, passar ele como argumento(pode ser passado mais de 1 arquivo)
```console
python main.py -u jKvcHQZP540, url_id.txt -m video -r 360, 720, 1080
```
![image](https://github.com/NinjaHKZ/YouTube-Downloader/assets/100825381/8a224bc3-2e73-4795-8561-2bb6c92bbc9d)
> A estrutura do arquivo deve ser dessa forma:
```html
https://www.youtube.com/watch?v=PPyuq7G0BZ0&ab_channel=RodrigoZin-Topic
https://www.youtube.com/watch?v=9p3l1lr9G1M&ab_channel=RodrigoZin
https://www.youtube.com/watch?v=pWomJnHKWsE&ab_channel=RodrigoZin
LT8C5kYwcpA&
LT8C5kYwcp
```

###### Esse projeto foi realizado com boas intenções, a utilização indevida do software é de responsabilidade do usuário.
