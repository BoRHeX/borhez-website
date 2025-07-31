
// auth.js
// Handles user authentication using Firebase Email/Password.
// Requires firebase-config.js to be loaded before this script.

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-auth.js";
import { firebaseConfig } from './firebase-config.js';

// Initialize Firebase app and auth service
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// DOM elements
const emailInput = document.getElementById('auth-email');
const passwordInput = document.getElementById('auth-password');
const registerButton = document.getElementById('auth-register');
const loginButton = document.getElementById('auth-login');
const logoutButton = document.getElementById('auth-logout');
const userInfo = document.getElementById('auth-user-info');
const errorMsg = document.getElementById('auth-error');

// Clear any existing errors
function showError(message) {
  if (errorMsg) {
    errorMsg.textContent = message;
    errorMsg.style.display = 'block';
  }
}

function clearError() {
  if (errorMsg) {
    errorMsg.textContent = '';
    errorMsg.style.display = 'none';
  }
}

// Register a new user
async function registerUser() {
  clearError();
  const email = emailInput.value;
  const password = passwordInput.value;
  try {
    await createUserWithEmailAndPassword(auth, email, password);
  } catch (error) {
    showError(error.message);
  }
}

// Log in an existing user
async function loginUser() {
  clearError();
  const email = emailInput.value;
  const password = passwordInput.value;
  try {
    await signInWithEmailAndPassword(auth, email, password);
  } catch (error) {
    showError(error.message);
  }
}

// Log out the current user
async function logoutUser() {
  clearError();
  try {
    await signOut(auth);
  } catch (error) {
    showError(error.message);
  }
}

// Attach button handlers once DOM is loaded
function initAuthUI() {
  if (registerButton) registerButton.addEventListener('click', registerUser);
  if (loginButton) loginButton.addEventListener('click', loginUser);
  if (logoutButton) logoutButton.addEventListener('click', logoutUser);
}

// Update the UI based on the user's auth status
function updateUI(user) {
  if (user) {
    // User is signed in
    userInfo.textContent = `Welcome, ${user.email}`;
    logoutButton.style.display = 'inline-block';
    loginButton.style.display = 'none';
    registerButton.style.display = 'none';
  } else {
    // No user is signed in
    userInfo.textContent = 'Not signed in';
    logoutButton.style.display = 'none';
    loginButton.style.display = 'inline-block';
    registerButton.style.display = 'inline-block';
  }
}

// Listen for auth state changes
onAuthStateChanged(auth, (user) => {
  updateUI(user);
});

// Initialize UI on DOMContentLoaded
window.addEventListener('DOMContentLoaded', () => {
  initAuthUI();
  // Show initial state
  updateUI(auth.currentUser);
});
