import sys #I don't remeber why I used this but is in many of my old codes so must be important at some point
import os #Server thing
import json #Database
import discord #One of the discord libraries
from keep_alive import keep_alive #Server (one of my old codes)
import random #Get random number (I still plan on doing something with it)
from discord.ext import commands #Second discord library

from openai import OpenAI

my_secret = os.environ['TOKEN']
my_openaikey = os.environ['OPENAIKEY']



#ChatGPT configs
chatgpt = OpenAI(api_key=my_openaikey)
#gpt-3.5-turbo-0125
#gpt-4o (maybe)
gpt4 = "gpt-4o"
gpt3 = "gpt-3.5-turbo-0125"
temperature = 0.3

max_tokens = 400

cont = "(Language=Pt-BR) Você é um Bot do programa de férias “Te Orienta nas Férias”, que prepara alunos para o ENEM (Exame Nacional do Ensino Médio) brasileiro. Seu papel é responder perguntas e dúvidas dos alunos."

contextResp = "(Lang=Pt-BR) Seu papel é responder questões,não use comandos Latex"
contextDuv = "(Lang=Pt-BR) Seu papel é responder dúvidas,não use comandos Latex"
contextImag = "(Lang=Pt-BR) O input será uma imagem,seu papel é responder as perguntas presentes na imagem, não use linguagem de formatação(como Latex)."

#Some intent bs that discord requires to run your bot
intents = discord.Intents.default() #Set intents as defined in the discord API website 
intents.message_content = True #Enable bot to see messsages

client = commands.Bot(command_prefix='!', intents=intents) #Prefix


client.remove_command('help')

@client.event
async def on_ready():
    print('Connected as {0.user}'.format(client)) #Confirm bot is running correctly




dvalue = "O comando !duvida é utilizado para esclarecer dúvidas específicas sobre conteúdos diversos. Ao utilizar esse comando, você pode obter explicações detalhadas sobre tópicos que está enfrentando dificuldades, incluindo esquemas passo a passo e a lógica por trás do conteúdo." 

rvalue = "O comando !resolva é utilizado para obter a resolução completa de uma questão específica do modelo ENEM. Ao usar este comando, o bot fornecerá a resolução detalhada e a resposta correta para a questão informada, ajudando você a entender como chegar à solução."

ivalue = "O comando !imagem é utilizado para explicar conteúdos e resolver questões do modelo ENEM a partir de imagens. Ao usar este comando, você pode enviar uma foto ou captura de tela da questão, e o bot fornecerá a resolução detalhada e a resposta correta."

@client.command()
async def version(ctx):
    await ctx.send("Version: 1.1.0")

@client.command()
async def help(ctx):
      em = discord.Embed(title = "Lista de Comandos", color=discord.Color.og_blurple())


      em.add_field(name = '!duvida', value = dvalue,inline=False)
      em.add_field(name = '!resolva', value = rvalue,inline=False)
      em.add_field(name = '!imagem', value = ivalue,inline=False)

      await ctx.send(embed = em) 

@client.command()
async def ajuda(ctx):
      em = discord.Embed(title = "Lista de Comandos", color=discord.Color.og_blurple())


      em.add_field(name = '!duvida', value = dvalue,inline=False)
      em.add_field(name = '!resolva', value = rvalue,inline=False)
      em.add_field(name = '!imagem', value = ivalue,inline=False)

      await ctx.send(embed = em) 


def get_chatgpt_response(prompt, context, mod):
  completion = chatgpt.chat.completions.create(
      model=mod,
      messages=[
          {"role": "system", "content": context},
          {"role": "user", "content": prompt}
      ],
      temperature=temperature,
      max_tokens=max_tokens
  )
  return completion.choices[0].message.content
  
@client.command()
async def resolva(ctx, *, prompt):
  prompt = str(prompt)
  answer = get_chatgpt_response(prompt, contextResp, gpt4)
  await ctx.send(answer)

@client.command()
async def duvida(ctx, *, prompt):
  prompt = str(prompt)
  answer = get_chatgpt_response(prompt, contextDuv, gpt3)
  await ctx.send(answer)


def get_chatgpt_response_image(prompt, context, mod):
  completion = chatgpt.chat.completions.create(
      model=mod,
      messages=[
          {"role": "system", "content": context},
          {"role": "user", "content": [
              {
                  "type": "text",
                  "text": "Responda as questões"
                },
              {"type": "image_url", "image_url": {"url": prompt}}
          ]}
      ],
      temperature=temperature,
      max_tokens=max_tokens
  )
  return completion.choices[0].message.content

@client.command(name='imagem')
async def imagem(ctx):
    if not ctx.message.attachments:
        await ctx.send('Please attach an image.')
        return

    for attachment in ctx.message.attachments:
        if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
            # Save the image
            #await attachment.save(attachment.filename)

            # Here you can add any image processing you want to perform

            image_url = attachment.url
            answer = get_chatgpt_response_image(image_url, contextImag, gpt4)
            await ctx.send(answer)
        else:
            await ctx.send('Por favor mande um arquivo do formato adequado (png, jpg, jpeg, gif, bmp).')


keep_alive()

client.run(my_secret)    