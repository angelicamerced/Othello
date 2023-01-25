class AI {
  constructor(_player) {
    this.player = _player;
    this.opponent = (_player % 2) + 1;
    this.depth = 2;
  }

  minimax(oldBoard, depth, alpha, beta, maximizingPlayer) {
    if (!oldBoard.isGameOver() || depth == 0) {
      return this.heuristics(oldBoard);
    }
    //Calculate heuristic for each openset of the current min/max
    if (maximizingPlayer == true) {
      let validMoves = oldBoard.validMoves(this.player);
      if (validMoves.length == 0) {
        let nBoard = _.cloneDeep(oldBoard);
        return max(
          this.heuristics(nBoard),
          this.minimax(nBoard, depth - 1, alpha, beta, false)
        );
      } else {
        let maxE = -Infinity;
        for (let i = 0; i < validMoves.length; i++) {
          let tempBoard = _.cloneDeep(board);
          tempBoard.place(validMoves[i][0], validMoves[i][1], this.player);
          let evalu = max(
            this.heuristics(tempBoard),
            this.minimax(tempBoard, depth - 1, alpha, beta, false)
          ); //this.minimax(tempBoard, depth-1, alpha, beta, false); */
          maxE = max(maxE, evalu);
          //console.log("maxE", maxE);
          alpha = max(alpha, evalu);
          //console.log("alpha", alpha);
          if (beta <= alpha) break;
        }
        return maxE;
      }
    } else {
      let validMoves = oldBoard.validMoves(this.opponent);
      if (validMoves.length == 0) {
        let nBoard = _.cloneDeep(oldBoard);
        return min(
          this.heuristics(nBoard),
          this.minimax(nBoard, depth - 1, alpha, beta, true)
        );
      } else {
        let minE = Infinity;
        for (let i = 0; i < validMoves.length; i++) {
          let tempBoard = _.cloneDeep(board);
          tempBoard.place(validMoves[i][0], validMoves[i][1], this.opponent);
          let evalu = min(
            this.heuristics(tempBoard),
            this.minimax(tempBoard, depth - 1, alpha, beta, true)
          );
          minE = min(minE, evalu);
          beta = min(beta, evalu);
          if (beta <= alpha) break;
        }
        return minE;
      }
    }
  }

  move() {
    let validMoves = board.validMoves(this.player);
    if (validMoves.length == 0) return false;
    let maxE = -Infinity;
    let sel = 0;
    for (let i = 0; i < validMoves.length; i++) {
      let tempBoard = _.cloneDeep(board);
      tempBoard.place(validMoves[i][0], validMoves[i][1], this.player);
      let evalu = this.minimax(
        tempBoard,
        this.depth - 1,
        -Infinity,
        Infinity,
        false
      );
      /* let evalu = max(this.heuristics(tempBoard), this.minimax(tempBoard, this.depth-1, -Infinity, Infinity, false)); */
      // console.log(evalu);
      if (evalu > maxE) sel = i;
      maxE = max(maxE, evalu);
    }
    // console.log(maxE);
    board.place(validMoves[sel][0], validMoves[sel][1], this.player);
    return true;
    // console.log("Placing "+validMoves[sel][0]+", "+validMoves[sel][1]);
  }

  heuristics(targetBoard) {
    let player_me = 0,
      player_ai = 0,
      my_front_tiles = 0,
      opp_front_tiles = 0,
      x,
      y;
    let p = 0,
      c = 0,
      l = 0,
      m = 0,
      f = 0,
      d = 0;

    let X1 = [-1, -1, 0, 1, 1, 1, 0, -1];
    let Y1 = [0, 1, 1, 1, 0, -1, -1, -1];

    let weights = [
      [20, -7, 11, 8, 8, 11, -7, 20],
      [-7, -10, -4, 1, 1, -4, -10, -7],
      [11, -4, 2, 2, 2, 2, -4, 11],
      [8, 1, 2, -3, -3, 2, 1, 8],
      [8, 1, 2, -3, -3, 2, 1, 8],
      [11, -4, 2, 2, 2, 2, -4, 11],
      [-7, -10, -4, 1, 1, -4, -10, -7],
      [20, -7, 11, 8, 8, 11, -7, 20],
    ];

    // PIECE DIFFERENCE
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        if (targetBoard.tiles[i * 8 + j].value == this.player) {
          // IF MY VALUE
          d += weights[i][j];
          player_me++;
        } else if (targetBoard.tiles[i * 8 + j].value == this.opponent) {
          d -= weights[i][j];
          player_ai++;
        }
        if (targetBoard.tiles[i * 8 + j].value > 0) {
          for (let k = 0; k < 8; k++) {
            x = i + X1[k];
            y = j + Y1[k];
            if (
              x >= 0 &&
              x < 8 &&
              y >= 0 &&
              y < 8 &&
              targetBoard.tiles[y * 8 + x] == 0
            ) {
              if (targetBoard.tiles[i * 8 + j] == this.player) my_front_tiles++;
              else opp_front_tiles++;
              break;
            }
          }
        }
      }
    }
    if (player_me > player_ai) p = (100.0 * player_me) / (player_me + player_ai);
    else if (player_me < player_ai)
      p = -(100.0 * player_ai) / (player_me + player_ai);
    else p = 0;

    if (my_front_tiles > opp_front_tiles)
      f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles);
    else if (my_front_tiles < opp_front_tiles)
      f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles);
    else f = 0;

    // CORNER OCCUPANCY
    player_me = 0;
    player_ai = 0;

    if (targetBoard.tiles[0].value == this.player) player_me++;
    else if (targetBoard.tiles[0].value == this.opponent) player_ai++;

    if (targetBoard.tiles[7 * 8].value == this.player) player_me++;
    else if (targetBoard.tiles[7 * 8].value == this.opponent) player_ai++;

    if (targetBoard.tiles[7].value == this.player) player_me++;
    else if (targetBoard.tiles[7].value == this.opponent) player_ai++;

    if (targetBoard.tiles[7 * 8 + 7].value == this.player) player_me++;
    else if (targetBoard.tiles[7 * 8 + 7].value == this.opponent) player_ai++;

    c = 25 * (player_me - player_ai);

    // CORNER CLOSENESS
    player_me = 0;
    player_ai = 0;

    if (targetBoard.tiles[0].value == 0) {
      if (targetBoard.tiles[1].value == this.player) player_me++;
      else if (targetBoard.tiles[1].value == this.opponent) player_ai++;
      if (targetBoard.tiles[1 * 8 + 1].value == this.player) player_me++;
      else if (targetBoard.tiles[1 * 8 + 1].value == this.opponent) player_ai++;
      if (targetBoard.tiles[8].value == this.player) player_me++;
      else if (targetBoard.tiles[8].value == this.opponent) player_ai++;
    }

    if (targetBoard.tiles[7].value == 0) {
      if (targetBoard.tiles[6].value == this.player) player_me++;
      else if (targetBoard.tiles[6].value == this.opponent) player_ai++;
      if (targetBoard.tiles[1 * 8 + 6].value == this.player) player_me++;
      else if (targetBoard.tiles[1 * 8 + 6].value == this.opponent) player_ai++;
      if (targetBoard.tiles[1 * 8 + 7].value == this.player) player_me++;
      else if (targetBoard.tiles[1 * 8 + 7].value == this.opponent) player_ai++;
    }

    if (targetBoard.tiles[7 * 8].value == 0) {
      if (targetBoard.tiles[7 * 8 + 1].value == this.player) player_me++;
      else if (targetBoard.tiles[7 * 8 + 1].value == this.opponent) player_ai++;
      if (targetBoard.tiles[6 * 8 + 1].value == this.player) player_me++;
      else if (targetBoard.tiles[6 * 8 + 1].value == this.opponent) player_ai++;
      if (targetBoard.tiles[6 * 8].value == this.player) player_me++;
      else if (targetBoard.tiles[6 * 8].value == this.opponent) player_ai++;
    }

    if (targetBoard.tiles[7 * 8 + 7].value == 0) {
      if (targetBoard.tiles[6 * 8 + 7].value == this.player) player_me++;
      else if (targetBoard.tiles[6 * 8 + 7].value == this.opponent) player_ai++;
      if (targetBoard.tiles[6 * 8 + 6].value == this.player) player_me++;
      else if (targetBoard.tiles[6 * 8 + 6].value == this.opponent) player_ai++;
      if (targetBoard.tiles[7 * 8 + 6].value == this.player) player_me++;
      else if (targetBoard.tiles[7 * 8 + 6].value == this.opponent) player_ai++;
    }

    l = -12.5 * (player_me - player_ai);

    // Heuristic function - Mobility
    player_me = targetBoard.validMoves(this.player).length;
    player_ai = targetBoard.validMoves(this.opponent).length;

    if (player_me > player_ai) {
      mob_heur = (100.0 * player_me) / (player_me + player_ai);
    } else if (player_me < player_ai) {
      mob_heur = -(100.0 * player_me) / (player_me + player_ai);
    } else {
      mob_heur = 0;
    }
    // FINAL WEIGHTED SCORE
    let score =
      10 * p + 801.724 * c + 382.026 * l + 78.922 * mob_heur + 74.396 * f + 10 * d;
    return score;
  }
}
