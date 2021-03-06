from Player import Player
from copy import deepcopy
import math
from random import random
from decimal import *


MAX_DEPTH = 2

class MiniMaxPlayer(Player):
    INFINITY = math.inf
    
    #___________________________
    #______simple minimax_______   
    #___________________________

    def max_val(self, opponent, depth):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = -self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):
            
            self.play(action, is_evaluating=True)
            
            m = opponent.min_val(self, depth+1)
            if (m[0] > v):
                v = m[0]
                best_action = action
            
            self.undo_last_action()
            
        return v, best_action
    
    def min_val(self, opponent, depth):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):        
            self.play(action, is_evaluating=True)
            m = opponent.max_val(self, depth+1)
            if (m[0] < v):
                v = m[0]
                best_action = action
                
            self.undo_last_action()
            
        return v, best_action
    
    #____________________________
    #______forward pruning_______
    #____________________________

    def max_val_fp(self, opponent, depth):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = -self.INFINITY
        best_action = None
        i = 1
        for action in self.get_legal_actions(opponent):
            x = random()
            if (x*100 + math.sqrt(i) > 70):
                
                self.play(action, is_evaluating=True)
                
                m = opponent.min_val_fp(self, depth+1)
                if (m[0] > v):
                    v = m[0]
                    best_action = action
                
                self.undo_last_action()
            i+=1
            
        if best_action == None:
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                
                m = opponent.min_val_fp(self, depth+1)
                if (m[0] > v):
                    v = m[0]
                    best_action = action
                
                self.undo_last_action()
        
        return v, best_action
    
    def min_val_fp(self, opponent, depth):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = self.INFINITY
        best_action = None
        i = 1
        for action in self.get_legal_actions(opponent):        
            x = random()
            if (x*100 + math.sqrt(i) > 70):
                self.play(action, is_evaluating=True)
                m = opponent.max_val_fp(self, depth+1)
                if (m[0] < v):
                    v = m[0]
                    best_action = action
                    
                self.undo_last_action()
            i+=1
        
        if best_action == None:
            for action in self.get_legal_actions(opponent):        
                self.play(action, is_evaluating=True)
                m = opponent.max_val_fp(self, depth+1)
                if (m[0] < v):
                    v = m[0]
                    best_action = action
                    
                self.undo_last_action()
        
        return v, best_action
    
    
    #_______________________________
    #______alpha beta pruning_______
    #_______________________________

    
    def max_val_abp(self, opponent, alpha, beta, depth):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = -self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):
            
            self.play(action, is_evaluating=True)
            
            m = opponent.min_val_abp(self, alpha, beta, depth+1)
            if (m[0] > v):
                v = m[0]
                best_action = action
            self.undo_last_action()
            
            alpha = max(alpha, m[0])
            if beta <= alpha:
                break
            
        return v, best_action
    
    def min_val_abp(self, opponent, alpha, beta, depth):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):        
            self.play(action, is_evaluating=True)
            m = opponent.max_val_abp(self, alpha, beta, depth+1)
            if (m[0] < v):
                v = m[0]
                best_action = action
            
            self.undo_last_action()
            beta = min(beta, m[0])
            if beta <= alpha:
                break
            
            
        return v, best_action

    
    #____________________________
    #_____alpha beta + table_____
    #____________________________

    
    def max_val_abp_table(self, opponent, alpha, beta, depth, table):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = -self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            
            if table.get(hash) != None:
                m = table.get(hash), None
            else:
                m = opponent.min_val_abp_table(self, alpha, beta, depth+1, table)
                table[str(hash)] = m[0]
                
            if (m[0] > v):
                v = m[0]
                best_action = action
            self.undo_last_action()
            
            alpha = max(alpha, m[0])
            if beta <= alpha:
                break
            
        return v, best_action
    
    def min_val_abp_table(self, opponent, alpha, beta, depth, table):
        if (depth == MAX_DEPTH):
            return self.evaluate(opponent), None
        
        v = self.INFINITY
        best_action = None
        for action in self.get_legal_actions(opponent):        
            self.play(action, is_evaluating=True)
            
            hash = self.get_board().get_hash()
            
            if table.get(hash) != None:
                m = table.get(hash), None
            else:
                m = opponent.max_val_abp_table(self, alpha, beta, depth+1, table)
                table[str(hash)] = m[0]
            
            if (m[0] < v):
                v = m[0]
                best_action = action
            
            self.undo_last_action()
            beta = min(beta, m[0])
            if beta <= alpha:
                break
            
        return v, best_action


    def bfs(self, opponent: Player):
        self_distance = 0
        opponent_distance = 0
        for player in [self, opponent]:
            destination = (
                self.board.get_white_goal_pieces()
                if player.color == "white"
                else self.board.get_black_goal_pieces()
            )
            
            visited = {}
            distances = {}
            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for i in self.board.get_piece_neighbors(piece):
                    if visited[i] == False:
                        distances[i] = distances[piece] + 1
                        visited[i] = True
                        queue.append(i)

            min_distance = self.INFINITY
            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            
            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance

        return self_distance, opponent_distance

    def evaluate(self, opponent:Player):
        result = 0
        self_distance, opponent_distance = self.bfs(opponent)
        
        if self_distance != 0:
            result += round(100/self_distance, 4)
        else:
            result += 1000
            
            
        if opponent_distance != 0:
            result -= round(50/opponent_distance, 4)
        else:
            result -= 500
            
        result += (self.walls_count - opponent.walls_count)*10
        result -= self.walls_count * 5
        
        return result
    
    def get_best_action(self, opponent, mode):
        best_action = None
        if mode == 'm':
            v, best_action = self.max_val(opponent, 0)
        elif mode == 'abp':
            v, best_action = self.max_val_abp(opponent, -self.INFINITY, self.INFINITY, 0)
        elif mode == 'fp':
            v, best_action = self.max_val_fp(opponent, 0)
        elif mode == 'table':
            table = dict()
            v, best_action = self.max_val_abp_table(opponent, -self.INFINITY, self.INFINITY, 0, table)

            
        
        
        return best_action        
        