# Pong

Jogo clássico de Pong desenvolvido em Python com Pygame.

## Requisitos

- Python
- Pygame

## Instalação

```bash
pip install pygame
```

## Como Jogar

Execute o jogo:

```bash
python main.py
```

### Controles

| Tecla               | Ação                                |
| ------------------- | ----------------------------------- |
| ↑ (Seta para cima)  | Move o paddle do jogador para cima  |
| ↓ (Seta para baixo) | Move o paddle do jogador para baixo |

O jogador controla o paddle da esquerda. O paddle da direita é controlado pela IA.

## Estrutura do Projeto

```
PONG/
├── main.py      # Ponto de entrada do jogo
├── game.py      # Classes e lógica do jogo
└── README.md    # Documentação
```

## Classes

### `Paddle`

Representa as raquetes dos jogadores.

- Dimensões: 10x60 pixels
- Velocidade: 5 pixels/frame

### `Ball`

Representa a bola do jogo.

- Tamanho: 7 pixels de raio
- Velocidade inicial: 5 pixels/frame em ambos os eixos
- Inverte direção vertical ao colidir com bordas superior/inferior
- Inverte direção horizontal ao colidir com paddles

### `Score`

Gerencia a pontuação dos jogadores.

- Jogador 1 marca ponto quando a bola ultrapassa a borda direita
- Jogador 2 marca ponto quando a bola ultrapassa a borda esquerda

### `PongGame`

Classe principal que gerencia o loop do jogo.

- Resolução: 800x600 pixels
- Taxa de atualização: 60 FPS
