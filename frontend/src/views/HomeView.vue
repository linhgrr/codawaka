<template>
  <div class="home">
    <!-- Hero section with dark background -->
    <div class="hero-section">
      <div class="hero-background"></div>
      <div class="hero-overlay"></div>
      <div class="container">
        <div class="row justify-content-center text-center py-5">
          <div class="col-lg-10">
            <h1 class="hero-title animate-in fade-up delay-1">Just code it<br>with CodaWaka</h1>
            <p class="hero-tagline animate-in fade-up delay-2">The best tool to have in test</p>
            
            <div class="hero-buttons mt-4 animate-in fade-up delay-3">
              <div v-if="!isLoggedIn">
                <router-link to="/register" class="btn btn-primary btn-cta me-3">Start for free</router-link>
                <button @click="scrollToVideo" class="btn btn-dark btn-video">Watch video</button>
              </div>
              <div v-else>
                <router-link to="/generate" class="btn btn-primary btn-cta me-3">Generate Code</router-link>
                <router-link to="/history" class="btn btn-dark btn-video">My History</router-link>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Editor interface preview image -->
        <div class="row justify-content-center">
          <div class="col-lg-11">
            <div id="video-section" class="editor-preview animate-in fade-up delay-4">
              <div class="date-badge">May 2, 2025: Introducing Codawaka</div>
              <div class="video-container">
                <iframe 
                  id="intro-video"
                  ref="youtubeVideo"
                  width="100%" 
                  height="600" 
                  src="https://www.youtube.com/embed/tyITq3LCWXo" 
                  title="Codawaka Introduction" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                  allowfullscreen>
                </iframe>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features section -->
    <div class="features-section py-5">
      <div class="container">
        <div class="section-header text-center animate-in fade-up">
          <h6 class="section-subtitle">Features</h6>
          <h2 class="section-title">Key Features</h2>
          <div class="section-divider"></div>
        </div>
        
        <div class="row g-4 mt-3">
          <div class="col-md-4 animate-in fade-up delay-1">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-rocket"></i>
              </div>
              <h3>Instant Code Generation</h3>
              <p>Simply describe your requirements and the AI will generate high-quality code in seconds.</p>
            </div>
          </div>
          <div class="col-md-4 animate-in fade-up delay-2">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-code-branch"></i>
              </div>
              <h3>Multiple Languages</h3>
              <p>Supports a wide range of popular programming languages including Python, JavaScript, Java, C++, and more.</p>
            </div>
          </div>
          <div class="col-md-4 animate-in fade-up delay-3">
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
        <div class="section-header text-center animate-in fade-up">
          <h6 class="section-subtitle">Process</h6>
          <h2 class="section-title">How It Works</h2>
          <div class="section-divider"></div>
        </div>
        
        <div class="row g-4 mt-4">
          <div class="col-md-4 animate-in fade-up delay-1">
            <div class="step-card">
              <div class="step-number">01</div>
              <h3>Describe Requirements</h3>
              <p>Enter a detailed description of the code or algorithm you need to create.</p>
            </div>
          </div>
          <div class="col-md-4 animate-in fade-up delay-2">
            <div class="step-card">
              <div class="step-number">02</div>
              <h3>AI Processing</h3>
              <p>Our advanced AI system analyzes your requirements and generates optimized code.</p>
            </div>
          </div>
          <div class="col-md-4 animate-in fade-up delay-3">
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
          <div class="col-lg-8 animate-in fade-up delay-1">
            <h2 class="cta-title">Ready to experience the power of AI?</h2>
            <p class="cta-text">Create a free account and get 10 credits to start.</p>
          </div>
          <div class="col-lg-4 text-lg-end mt-4 mt-lg-0 animate-in fade-up delay-2">
            <router-link to="/register" class="btn btn-lg btn-primary btn-cta">Sign Up Now</router-link>
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
  methods: {
    scrollToVideo() {
      // Get the video element
      const videoSection = document.getElementById('video-section');
      if (videoSection) {
        // Scroll to video with smooth behavior
        videoSection.scrollIntoView({ behavior: 'smooth' });
        
        // Add a slight delay before playing the video to allow scrolling to complete
        setTimeout(() => {
          // Get the iframe element
          const iframe = this.$refs.youtubeVideo;
          
          // Update the src to autoplay the video
          if (iframe) {
            let currentSrc = iframe.src;
            if (currentSrc.indexOf('autoplay=1') === -1) {
              // If autoplay parameter doesn't exist, add it
              iframe.src = currentSrc + (currentSrc.includes('?') ? '&' : '?') + 'autoplay=1';
            }
          }
        }, 800); // Delay of 800ms
      }
    }
  },
}
</script>

<style scoped>
.hero-section {
  position: relative;
  background-color: var(--dark-bg);
  color: var(--dark-text);
  padding: 120px 0 70px;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/wallpaper.avif');
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(5, 5, 10, 0.7), rgba(10, 10, 20, 0.9));
  z-index: 2;
}

.hero-section .container {
  position: relative;
  z-index: 3;
}

.hero-title {
  font-size: 5rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 20px;
  color: var(--dark-text);
  letter-spacing: -0.03em;
  z-index: 3;
  position: relative;
}

.hero-tagline {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  color: var(--dark-text-secondary);
  font-weight: normal;
  letter-spacing: -0.01em;
  z-index: 3;
  position: relative;
}

.btn-cta {
  padding: 12px 24px;
  font-weight: 500;
  border-radius: 50px;
  background: var(--primary-color);
  color: white;
  border: none;
  transition: all 0.2s ease;
  letter-spacing: -0.01em;
}

.btn-cta:hover {
  background: var(--primary-color-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  color: white;
}

.btn-video {
  padding: 12px 24px;
  font-weight: 500;
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.08);
  color: var(--dark-text);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all 0.2s ease;
  letter-spacing: -0.01em;
}

.btn-video:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.2);
}

.editor-preview {
  margin-top: 60px;
  position: relative;
}

.date-badge {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.08);
  padding: 8px 16px;
  border-radius: 30px;
  color: var(--dark-text-secondary);
  font-size: 0.9rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.video-container {
  width: 100%;
  height: 600px;
  background-color: var(--dark-card-bg);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--dark-border);
}

/* Animation styles */
.animate-in {
  opacity: 0;
  transform: translateY(30px);
}

.fade-up {
  animation: fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.delay-1 {
  animation-delay: 0.2s;
}

.delay-2 {
  animation-delay: 0.4s;
}

.delay-3 {
  animation-delay: 0.6s;
}

.delay-4 {
  animation-delay: 0.8s;
}

/* Features Section */
.features-section {
  background-color: var(--dark-bg);
  padding: 100px 0;
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
  border-radius: 8px;
  padding: 24px;
  height: 100%;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: rgba(94, 92, 230, 0.3);
}

.feature-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(94, 92, 230, 0.1);
  border-radius: 8px;
  font-size: 1.25rem;
  color: var(--primary-color);
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--dark-text);
  letter-spacing: -0.01em;
}

.feature-card p {
  color: var(--dark-text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
}

/* How it works section */
.how-it-works-section {
  background-color: var(--dark-card-secondary);
  padding: 80px 0;
}

.step-card {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  border-radius: 8px;
  padding: 24px;
  height: 100%;
  transition: all 0.2s ease;
}

.step-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: rgba(94, 92, 230, 0.3);
}

.step-number {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--primary-color);
  opacity: 0.9;
  letter-spacing: -0.02em;
}

.step-card h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--dark-text);
  letter-spacing: -0.01em;
}

.step-card p {
  color: var(--dark-text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
}

/* CTA Section */
.cta-section {
  background-color: var(--dark-card-bg);
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  margin: 40px 20px;
  border: 1px solid var(--dark-border);
  padding: 50px 30px;
}

.cta-glow {
  position: absolute;
  top: -100px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(94, 92, 230, 0.12), transparent 70%);
  border-radius: 50%;
  z-index: 0;
}

.cta-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--dark-text);
  letter-spacing: -0.02em;
  position: relative;
  z-index: 1;
}

.cta-text {
  font-size: 1.1rem;
  color: var(--dark-text-secondary);
  position: relative;
  z-index: 1;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .hero-title {
    font-size: 3.5rem;
  }
  
  .cta-title {
    font-size: 1.8rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 70px 0 50px;
  }
  
  .hero-title {
    font-size: 2.8rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
}
</style>