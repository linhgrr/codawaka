<template>
  <div class="home">
    <!-- Hero section with polygon visual effect -->
    <div class="hero-section">
      <div class="polygon-particles"></div>
      <div class="hero-glow-1"></div>
      <div class="hero-glow-2"></div>
      
      <div class="container">
        <div class="row py-5">
          <div class="col-lg-6 hero-content">
            <div class="hero-badge">AI Agent</div>
            <h1 class="hero-title">Code Generator AI</h1>
            <p class="hero-tagline">"Thuật toán ứng dụng, đụng tool là xong"</p>
            <p class="hero-description">
              Intelligent coding platform leveraging the power of AI Agents to solve complex programming problems in just seconds.
            </p>
            <div class="hero-buttons mt-4">
              <div v-if="!isLoggedIn">
                <router-link to="/login" class="btn btn-primary btn-glow me-3">Login</router-link>
                <router-link to="/register" class="btn btn-outline-glow">Sign Up</router-link>
              </div>
              <div v-else>
                <router-link to="/generate" class="btn btn-primary btn-glow me-3">Generate Code</router-link>
                <router-link to="/history" class="btn btn-outline-glow">History</router-link>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="video-container mt-4 mt-lg-0">
              <div class="glow-border"></div>
              <iframe 
                width="100%" 
                height="315" 
                src="https://youtu.be/tyITq3LCWXo" 
                title="Code Generator Tutorial" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
              </iframe>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Counter -->
    <div class="stats-section">
      <div class="container">
        <div class="row stats-row">
          <div class="col-md-4 mb-4 mb-md-0">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-code"></i>
              </div>
              <div class="stat-number">50+</div>
              <div class="stat-title">Programming Languages</div>
            </div>
          </div>
          <div class="col-md-4 mb-4 mb-md-0">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-bolt"></i>
              </div>
              <div class="stat-number">0.5s</div>
              <div class="stat-title">Response Time</div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-users"></i>
              </div>
              <div class="stat-number">10k+</div>
              <div class="stat-title">Users</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features section -->
    <div class="features-section py-5">
      <div class="container">
        <div class="section-header text-center">
          <h6 class="section-subtitle">Features</h6>
          <h2 class="section-title">Key Features</h2>
          <div class="section-divider"></div>
        </div>
        
        <div class="row g-4 mt-3">
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-rocket"></i>
              </div>
              <h3>Instant Code Generation</h3>
              <p>Simply describe your requirements and the AI will generate high-quality code in seconds.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-code-branch"></i>
              </div>
              <h3>Multiple Languages</h3>
              <p>Supports a wide range of popular programming languages including Python, JavaScript, Java, C++, and more.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-shield-alt"></i>
              </div>
              <h3>Maximum Security</h3>
              <p>Your source code is securely protected and not stored beyond the required time period.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- How it works section -->
    <div class="how-it-works-section py-5">
      <div class="container">
        <div class="section-header text-center">
          <h6 class="section-subtitle">Process</h6>
          <h2 class="section-title">How It Works</h2>
          <div class="section-divider"></div>
        </div>
        
        <div class="row g-4 mt-4">
          <div class="col-md-4">
            <div class="step-card">
              <div class="step-number">01</div>
              <h3>Describe Requirements</h3>
              <p>Enter a detailed description of the code or algorithm you need to create.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card">
              <div class="step-number">02</div>
              <h3>AI Processing</h3>
              <p>Our advanced AI system analyzes your requirements and generates optimized code.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="step-card">
              <div class="step-number">03</div>
              <h3>Get Results</h3>
              <p>Receive high-quality code, ready to use in your project.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="cta-section py-5">
      <div class="cta-glow"></div>
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-8">
            <h2 class="cta-title">Ready to experience the power of AI?</h2>
            <p class="cta-text">Create a free account and get 10 credits to start.</p>
          </div>
          <div class="col-lg-4 text-lg-end mt-4 mt-lg-0">
            <router-link to="/register" class="btn btn-lg btn-primary btn-glow">Sign Up Now</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'HomeView',
  computed: {
    ...mapGetters(['isLoggedIn']),
  },
}
</script>

<style scoped>
.hero-section {
  position: relative;
  background-color: var(--dark-bg);
  color: var(--dark-text);
  padding: 100px 0 120px;
  overflow: hidden;
}

.polygon-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><polygon points="10,1 19,10 10,19 1,10" stroke="rgba(123,63,228,0.15)" stroke-width="1" fill="none" /></svg>');
  background-size: 80px 80px;
  opacity: 0.5;
  animation: floatParticles 30s linear infinite;
}

.hero-glow-1, .hero-glow-2 {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.hero-glow-1 {
  top: -150px;
  left: -100px;
  width: 500px;
  height: 500px;
  background: rgba(123, 63, 228, 0.2);
}

.hero-glow-2 {
  bottom: -200px;
  right: -100px;
  width: 600px;
  height: 600px;
  background: rgba(167, 38, 193, 0.15);
}

.hero-content {
  position: relative;
  z-index: 10;
  padding-top: 40px;
}

.hero-badge {
  display: inline-block;
  background: rgba(123, 63, 228, 0.15);
  color: var(--primary-color);
  font-size: 0.85rem;
  font-weight: 600;
  padding: 6px 15px;
  border-radius: 30px;
  margin-bottom: 20px;
  border: 1px solid rgba(123, 63, 228, 0.3);
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 20px;
  background: linear-gradient(90deg, #7b3fe4, #a726c1, #7b3fe4);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientFlow 5s ease infinite;
}

.hero-tagline {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
  color: var(--primary-color);
}

.hero-description {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  color: var(--dark-text-secondary);
  max-width: 90%;
}

.btn-glow {
  padding: 12px 30px;
  font-weight: 600;
  border-radius: 8px;
  background: var(--primary-gradient);
  border: none;
  box-shadow: 0 5px 20px var(--glow-color);
  transition: all 0.3s ease;
}

.btn-glow:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px var(--glow-color);
}

.btn-outline-glow {
  padding: 12px 30px;
  font-weight: 600;
  border-radius: 8px;
  background: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
  transition: all 0.3s ease;
}

.btn-outline-glow:hover {
  background: rgba(123, 63, 228, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(123, 63, 228, 0.2);
}

.video-container {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  z-index: 10;
}

.glow-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--primary-gradient);
  border-radius: 18px;
  z-index: -1;
  opacity: 0.7;
  animation: pulseBorder 2s ease-in-out infinite;
}

/* Stats Section */
.stats-section {
  background-color: var(--dark-card-bg);
  transform: translateY(-50px);
  z-index: 20;
  position: relative;
  border-radius: 16px;
}

.stats-row {
  background: linear-gradient(90deg, rgba(123, 63, 228, 0.05), rgba(167, 38, 193, 0.05));
  border-radius: 16px;
  padding: 30px 20px;
  margin: 0 5px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(123, 63, 228, 0.1);
}

.stat-card {
  text-align: center;
  padding: 15px;
}

.stat-icon {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 10px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 5px;
}

.stat-title {
  color: var(--dark-text-secondary);
  font-size: 1rem;
}

/* Features Section */
.features-section {
  background-color: var(--dark-bg);
  padding: 60px 0;
  position: relative;
  z-index: 10;
}

.section-header {
  margin-bottom: 40px;
}

.section-subtitle {
  color: var(--primary-color);
  text-transform: uppercase;
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 1px;
  margin-bottom: 10px;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--dark-text);
  margin-bottom: 15px;
}

.section-divider {
  width: 80px;
  height: 3px;
  background: var(--primary-gradient);
  margin: 0 auto;
  border-radius: 3px;
}

.feature-card {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  padding: 30px;
  height: 100%;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(123, 63, 228, 0.05), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  border-color: rgba(123, 63, 228, 0.3);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(123, 63, 228, 0.1);
  border-radius: 12px;
  font-size: 1.5rem;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--dark-text);
}

.feature-card p {
  color: var(--dark-text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* How it works section */
.how-it-works-section {
  background-color: var(--dark-card-bg);
  padding: 80px 0;
}

.step-card {
  background-color: var(--dark-bg);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  padding: 30px;
  height: 100%;
  transition: all 0.3s ease;
}

.step-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border-color: rgba(123, 63, 228, 0.3);
}

.step-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 15px;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  opacity: 0.8;
}

.step-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--dark-text);
}

.step-card p {
  color: var(--dark-text-secondary);
  font-size: 0.95rem;
}

/* CTA Section */
.cta-section {
  background-color: var(--dark-bg);
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  margin: 40px 20px;
  border: 1px solid var(--dark-border);
}

.cta-glow {
  position: absolute;
  top: -100px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(123, 63, 228, 0.15), transparent 70%);
  border-radius: 50%;
}

.cta-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--dark-text);
}

.cta-text {
  font-size: 1.1rem;
  color: var(--dark-text-secondary);
}

/* Animations */
@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes floatParticles {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 500px 500px;
  }
}

@keyframes pulseBorder {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-content {
    padding-top: 0;
  }
  
  .stats-section {
    transform: translateY(-30px);
  }
  
  .cta-title {
    font-size: 1.8rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 70px 0 100px;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
}
</style>