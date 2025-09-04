import streamlit as st
import random
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors Game",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .game-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin: 1rem 0;
    }
    .choice-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        border: none;
        color: white;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        border-radius: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.5rem;
        min-width: 120px;
    }
    .choice-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .result-display {
        background: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .score-display {
        background: rgba(255,255,255,0.15);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .emoji-large {
        font-size: 4rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for game data
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'ties' not in st.session_state:
    st.session_state.ties = 0
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

def get_computer_choice():
    """Get random choice for computer"""
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player_choice, computer_choice):
    """Determine the winner of the game"""
    if player_choice == computer_choice:
        return 'tie'
    
    winning_combinations = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    if winning_combinations[player_choice] == computer_choice:
        return 'player'
    else:
        return 'computer'

def get_emoji(choice):
    """Get emoji for each choice"""
    emojis = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    return emojis.get(choice, '❓')

def get_result_message(result, player_choice, computer_choice):
    """Get appropriate message based on game result"""
    if result == 'tie':
        return f"It's a tie! Both chose {get_emoji(player_choice)}"
    elif result == 'player':
        return f"You win! {get_emoji(player_choice)} beats {get_emoji(computer_choice)}"
    else:
        return f"Computer wins! {get_emoji(computer_choice)} beats {get_emoji(player_choice)}"

def play_game(player_choice):
    """Play one round of the game"""
    computer_choice = get_computer_choice()
    result = determine_winner(player_choice, computer_choice)
    
    # Update scores
    if result == 'player':
        st.session_state.player_score += 1
    elif result == 'computer':
        st.session_state.computer_score += 1
    else:
        st.session_state.ties += 1
    
    # Store game result
    game_result = {
        'timestamp': datetime.now(),
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result
    }
    st.session_state.game_history.append(game_result)
    
    return computer_choice, result

def reset_game():
    """Reset all game scores and history"""
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.ties = 0
    st.session_state.game_history = []
    st.session_state.last_result = None

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">✂️ Rock Paper Scissors ✂️</h1>', unsafe_allow_html=True)
    
    # Sidebar for game controls
    with st.sidebar:
        st.header("🎮 Game Controls")
        
        if st.button("🔄 Reset Game", use_container_width=True):
            reset_game()
            st.success("Game reset! All scores cleared.")
        
        st.markdown("---")
        st.header("📊 Statistics")
        st.metric("Total Games", len(st.session_state.game_history))
        st.metric("Win Rate", f"{(st.session_state.player_score / max(1, len(st.session_state.game_history))) * 100:.1f}%" if st.session_state.game_history else "0%")
        
        st.markdown("---")
        st.header("📈 Recent Games")
        if st.session_state.game_history:
            recent_games = st.session_state.game_history[-5:]  # Show last 5 games
            for game in reversed(recent_games):
                result_emoji = "🟢" if game['result'] == 'player' else "🔴" if game['result'] == 'computer' else "🟡"
                st.write(f"{result_emoji} {game['player_choice'].title()} vs {game['computer_choice'].title()} - {game['result'].title()}")
        else:
            st.write("No games played yet!")
    
    # Main game area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        
        # Score display
        st.markdown('<div class="score-display">', unsafe_allow_html=True)
        col_score1, col_score2, col_score3 = st.columns(3)
        
        with col_score1:
            st.metric("👤 Player", st.session_state.player_score)
        with col_score2:
            st.metric("🤖 Computer", st.session_state.computer_score)
        with col_score3:
            st.metric("🤝 Ties", st.session_state.ties)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Game choices
        st.subheader("🎯 Make Your Choice!")
        
        col_choice1, col_choice2, col_choice3 = st.columns(3)
        
        with col_choice1:
            if st.button("🪨 Rock", key="rock", use_container_width=True):
                computer_choice, result = play_game('rock')
                st.session_state.last_result = ('rock', computer_choice, result)
                st.rerun()
        
        with col_choice2:
            if st.button("📄 Paper", key="paper", use_container_width=True):
                computer_choice, result = play_game('paper')
                st.session_state.last_result = ('paper', computer_choice, result)
                st.rerun()
        
        with col_choice3:
            if st.button("✂️ Scissors", key="scissors", use_container_width=True):
                computer_choice, result = play_game('scissors')
                st.session_state.last_result = ('scissors', computer_choice, result)
                st.rerun()
        
        # Display last game result
        if st.session_state.last_result:
            player_choice, computer_choice, result = st.session_state.last_result
            
            st.markdown('<div class="result-display">', unsafe_allow_html=True)
            st.subheader("🎯 Last Round Result")
            
            col_result1, col_result2, col_result3 = st.columns(3)
            
            with col_result1:
                st.markdown(f"<div class='emoji-large'>{get_emoji(player_choice)}</div>", unsafe_allow_html=True)
                st.write("**Your Choice**")
                st.write(player_choice.title())
            
            with col_result2:
                st.markdown(f"<div class='emoji-large'>⚔️</div>", unsafe_allow_html=True)
                st.write("**VS**")
            
            with col_result3:
                st.markdown(f"<div class='emoji-large'>{get_emoji(computer_choice)}</div>", unsafe_allow_html=True)
                st.write("**Computer Choice**")
                st.write(computer_choice.title())
            
            # Result message
            result_message = get_result_message(result, player_choice, computer_choice)
            if result == 'player':
                st.success(f"🎉 {result_message}")
            elif result == 'computer':
                st.error(f"😔 {result_message}")
            else:
                st.info(f"🤝 {result_message}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Game instructions
    with st.expander("📖 How to Play"):
        st.markdown("""
        **Rock Paper Scissors** is a simple hand game usually played between two people.
        
        **Rules:**
        - 🪨 **Rock** crushes ✂️ **Scissors**
        - 📄 **Paper** covers 🪨 **Rock**
        - ✂️ **Scissors** cuts 📄 **Paper**
        
        **How to play:**
        1. Click on your choice (Rock, Paper, or Scissors)
        2. The computer will make its choice
        3. See who wins and track your score!
        4. Use the sidebar to reset the game or view statistics
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("🎮 **Rock Paper Scissors Game** - Built with Streamlit")
    st.markdown("💡 *Challenge yourself and see how many games you can win!*")

if __name__ == "__main__":
    main()
