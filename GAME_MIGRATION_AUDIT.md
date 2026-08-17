# Game Migration Audit

## Findings

### 1. `casino_play.html` was a second, fake game system
It contained client-side implementations for Aviator, Dice, Plinko, Slots,
Roulette, and several placeholder games. Those implementations used browser
`Math.random()` and local demo balances instead of the canonical server APIs.
This was the most important duplication and has been removed.

### 2. Canonical game implementations already existed
The real catalog has nine games and each already has a dedicated implementation:

| Catalog slug | Canonical UI | Canonical backend |
|---|---|---|
| `mzizicrash` | `games/crash_game.html` | `mzizicrash_blueprint.py` |
| `aviatormzizi` | `games/aviatormzizi.html` | `aviatormzizi_blueprint.py` |
| `jetx` | `games/jetx.html` | `jetx_blueprint.py` |
| `mines` | `games/mines.html` | `/api/casino/*` + `game_engine.py` |
| `dice` | `games/dice.html` | `/api/casino/*` + `game_engine.py` |
| `european-roulette` | `games/european-roulette.html` | `/api/casino/*` + `game_engine.py` |
| `hilocard` | `games/hilocard.html` | `hilocard_blueprint.py` |
| `plinkomzizi` | `games/plinkomzizi.html` | `plinkomzizi_blueprint.py` |
| `slots` | `games/slots.html` | `/api/casino/*` + `game_engine.py` |

### 3. Duplicate/dead route module
`app/routes/casino_blueprint.py` was not registered by the application factory
and implemented a different `/casino` architecture. It has been removed.

### 4. Duplicate templates
These duplicate/non-canonical root templates were removed:
- `app/templates/crash_game.html`
- `app/templates/cards.html`
- `app/templates/jetx.html`

The canonical versions remain under `app/templates/games/`.

### 5. Dormant Blackjack implementation
`cards_blueprint.py` and `cards_models.py` describe a Blackjack game, but the
current seeded catalog has no `cards` game and the application factory does not
register that blueprint. It is therefore outside the current canonical catalog.
It has not been promoted into the active registry.

### 6. Static asset organization
Three JavaScript files were incorrectly stored under `static/css/`. They were
moved to:
`app/static/js/games/`

## Result
The catalog now has one launch path and one canonical implementation per active
game. A missing implementation fails explicitly instead of silently falling
back to a fake browser game.

## Next phase
Refactor the nine canonical templates onto a shared responsive game shell:
header, balance, game field, betting controls, history, stats, and mobile
navigation. Game-specific JavaScript remains isolated per game.
