from typing import Optional

from selenium_manager import create_driver
import player_ids as ids


class Player:
    def __init__(
        self,
        name: Optional[str] = None,
        team: Optional[str] = None,
        pos_abbrv: Optional[str] = None,
        player_id: Optional[str] = None
        ):
        if not player_id:
            player_id = self._check_player(name, team, pos_abbrv)

    def _check_player(
        self,
        name: Optional[str],
        team: Optional[str],
        pos_abbrv: Optional[str]
        ):
        players_df = ids.get_current_players()
        if player_id:

