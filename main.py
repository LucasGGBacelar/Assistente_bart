import os
import pyttsx3
import time
import speech_recognition as sr
import pyautogui
import pygame
import threading
from bardapi import Bard
import random
import tkinter as tk
import PyPDF2

r = sr.Recognizer()
engine = pyttsx3.init()
limite_sem_audio = 1000
temporizador = time.time()

done_speaking = threading.Event()

engine.say("O que você deseja fazer?")
engine.runAndWait()

while True:
    with sr.Microphone() as source:
        audio = r.listen(source)
        comando = r.recognize_google(audio, language='pt-BR')

        # Verifica se o comando é uma ação
        if comando == "pausar":
            pyautogui.press('playpause')
            print("Executando ação...")
            engine.say("Pausando música...")
            engine.runAndWait()

        elif comando == "voltar":
            pyautogui.press('prevtrack')
            print("Voltando música...")
            engine.say("Voltando música...")
            engine.runAndWait()

        elif comando == "próxima":
            pyautogui.press('nexttrack')
            print("Avançando a música...")
            engine.say("Avançando música...")
            engine.runAndWait()


        elif comando == "pesquisa":
            engine.say("Diga o que você quer pesquisar")
            engine.runAndWait()
            audio = r.listen(source)
            palavra = r.recognize_google(audio, language='pt-BR')
            os.system("start chrome")
            time.sleep(2)
            pyautogui.write(palavra)
            pyautogui.press('enter')

        ######################################################################
        elif comando == "jogo":
            engine.runAndWait()
            pygame.init()


            def on_grid_random():
                x = random.randint(0, 590)
                y = random.randint(0, 590)
                return (x // 10 * 10, y // 10 * 10)


            def collision(c1, c2):
                return (c1[0] == c2[0]) and (c1[1] == c2[1])


            CIMA = 0
            DIREITA = 1
            BAIXO = 2
            ESQUERDA = 3

            pygame.init()
            screen = pygame.display.set_mode((500, 500))
            pygame.display.set_caption('Snake')

            # cobra
            cobra = [(200, 200), (210, 200), (220, 200)]
            snake_skin = pygame.Surface((10, 10))
            snake_skin.fill((0, 255, 0))

            # fruta
            fruta_pos = on_grid_random()
            fruta = pygame.Surface((10, 10))
            fruta.fill((255, 0, 0))

            my_direction = ESQUERDA

            clock = pygame.time.Clock()

            # Controles e saída
            while True:
                clock.tick(10)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()

                    if event.type == KEYDOWN:
                        if event.key == K_UP:
                            my_direction = CIMA
                        if event.key == K_DOWN:
                            my_direction = BAIXO
                        if event.key == K_LEFT:
                            my_direction = ESQUERDA
                        if event.key == K_RIGHT:
                            my_direction = DIREITA

                # colisao e aumento de tamanho
                if collision(cobra[0], fruta_pos):
                    fruta_pos = on_grid_random()
                    cobra.append(cobra[-1])

                # Direçoes/Movimentos
                for i in range(len(cobra) - 1, 0, -1):
                    cobra[i] = (cobra[i - 1][0], cobra[i - 1][1])

                if my_direction == CIMA:
                    cobra[0] = (cobra[0][0], cobra[0][1] - 10)
                if my_direction == BAIXO:
                    cobra[0] = (cobra[0][0], cobra[0][1] + 10)
                if my_direction == DIREITA:
                    cobra[0] = (cobra[0][0] + 10, cobra[0][1])
                if my_direction == ESQUERDA:
                    cobra[0] = (cobra[0][0] - 10, cobra[0][1])

                screen.fill((0, 0, 0))
                screen.blit(fruta, fruta_pos)
                for pos in cobra:
                    screen.blit(snake_skin, pos)

                pygame.display.update()

        ##################################################

        elif comando == "pergunta":

            os.environ['_BARD_API_KEY'] = "xxxxxx"
            engine.say("Faça a sua pergunta:")
            engine.runAndWait()

            # Faz o programa reconhecer seu áudio e transformá-lo em uma pergunta
            with sr.Microphone() as source:
                audio = r.listen(source)
                pergunta = r.recognize_google(audio, language='pt-BR')

                # Escreve e pergunta dita
                print(pergunta)

                # Usa a biblioteca BardAPI para gerar a resposta
                resposta = Bard().get_answer(pergunta)['content']

                # Imprime a resposta para o usuário
                print(resposta)

                # Sintetiza a resposta em voz alta
                engine.say(resposta)
                engine.runAndWait()
        ###########################################################################
        elif comando == "leitor de PDF":
            speaker = pyttsx3.init()
            engine.say('Diga o nome do livro')
            engine.runAndWait()

            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                nome_arquivo = r.recognize_google(audio, language='pt-BR') + '.pdf'
            except sr.UnknownValueError:
                print("Não foi possível reconhecer o áudio. Por favor, tente novamente.")
                nome_arquivo = None

            if nome_arquivo:
                livro = open(nome_arquivo, 'rb')
                pdfReader = PyPDF2.PdfFileReader(livro)
                paginas = pdfReader.numPages
                print(paginas)
                for num in range(0, paginas):
                    page = pdfReader.getPage(num)
                    texto = page.extractText()
                    speaker.say(texto)
                speaker.runAndWait()
        else:
            # Comando não reconhecido
            print(f"Unrecognized command: {comando}")
            engine.say("Comando não reconhecido.")
            engine.runAndWait()


