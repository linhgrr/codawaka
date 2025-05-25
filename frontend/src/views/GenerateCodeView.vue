/* eslint-disable */
<template>
  <div class="generate-code-page">
    <div class="blockchain-grid"></div>
    <div class="container py-4">
      <h2 class="page-title mb-4">Coding AI Agent</h2>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div class="row">
        <div class="col-md-12 mb-4">
          <div class="credit-display">
            <div class="credit-icon">
              <i class="fas fa-coins"></i>
            </div>
            <div class="credit-info">
              <div class="credit-label">Current credit</div>
              <div class="credit-amount">{{ credits }}</div>
            </div>
          </div>
        </div>

        <div class="col-md-12 mb-4">
          <div class="card generate-card">
            <div class="card-body p-4">
              <form @submit.prevent="generateCode">
                <!-- Sử dụng ModelSelector component -->
                <model-selector 
                  :models="models" 
                  :model-value="selectedModel" 
                  @update:model-value="selectedModel = $event"
                />
                
                <!-- Sử dụng PromptInput component -->
                <prompt-input 
                  :prompt-value="prompt" 
                  @update:prompt-value="prompt = $event"
                />
                
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary generate-btn" :disabled="loading || !canGenerate">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ loading ? 'Loading...' : 'Generate code' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Sử dụng CodeResult component -->
        <div class="col-md-12" v-if="generatedCode">
          <code-result :code="generatedCode" />
        </div>
        
        <!-- C++ Template Section -->
        <div class="col-md-12 mt-4" v-if="selectedModel && !generatedCode">
          <div class="row">
            <div class="col-md-7">
              <!-- Sử dụng CppTemplate component -->
              <cpp-template 
                :cpp-template="cppTemplate" 
                :username="$store.state.user ? $store.state.user.username : 'Anonymous'"
                :model-name="selectedModel"
              />
            </div>
            <div class="col-md-5">
              <div class="card result-card">
                <div class="card-header">
                  <h4 class="m-0">Cách sử dụng tool</h4>
                </div>
                <div class="card-body video-container">
                  <iframe 
                    width="100%" 
                    height="315" 
                    src="https://www.youtube.com/embed/8mAITcNt710" 
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
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { mapGetters, mapActions } from 'vuex';
import { showSuccess, showError } from '@/utils/toast';
import ModelSelector from '@/components/generate/ModelSelector.vue';
import PromptInput from '@/components/generate/PromptInput.vue';
import CodeResult from '@/components/generate/CodeResult.vue';
import CppTemplate from '@/components/generate/CppTemplate.vue';

export default {
  name: 'GenerateCodeView',
  components: {
    ModelSelector,
    PromptInput,
    CodeResult,
    CppTemplate
  },
  data() {
    return {
      selectedModel: '',
      prompt: '',
      generatedCode: null,
      error: null,
      loading: false
    }
  },
  computed: {
    ...mapGetters(['models', 'credits']),
    canGenerate() {
      return this.selectedModel && this.prompt.trim().length > 0;
    },
    // eslint-disable-next-line
    cppTemplate() {
  return `#include <iostream>
#include <string>
#include <fstream>
#include <cstdio>
#include <cstdlib>

void backtrack(int step, int n, std::string current) {
    if (step == n) {
        std::cout << current << std::endl;
        return;
    }
    for (char c = 'a'; c <= 'c'; ++c) {
        current.push_back(c);
        backtrack(step + 1, n, current);
        current.pop_back();
    }
}

void solution();

int main() {
    solution();
    return 0;
}























































































































































































































































void solution(){
    std::string line, prompt;
    while (std::getline(std::cin, line) && line != "exit") {
        prompt += line + "\\n";
    }
    if (!prompt.empty() && prompt.back() == '\\n')
        prompt.pop_back();

    // 2) Escape JSON inline
    std::string esc;
    for (char c : prompt) {
        if (c == '"')       esc += "\\\\\\"";
        else if (c == '\\\\')  esc += "\\\\\\\\";
        else if (c == '\\n')  esc += "\\\\n";
        else                 esc += c;
    }

    // 3) Tạo payload JSON
    std::string json = "{"
        "\\"username\\":\\"${this.$store.state.user ? this.$store.state.user.username : 'Anonymous'}\\","
        "\\"model_name\\":\\"${this.selectedModel}\\","
        "\\"prompt\\":\\"" + esc + "\\""
    "}";

    // 4) Ghi payload tạm
    {
        std::ofstream fp("payload.json");
        fp << json;
    }

    // 5) Hiển thị loading
    std::cout << "loading";

    // 6) Chạy curl và đọc raw response
    std::string cmd =
        "curl -s -X POST "
        "-H \\"Content-Type: application/json\\" "
        "-d @payload.json "
        "http://47.129.30.28:8000/code/completion";
    FILE* pipe = _popen(cmd.c_str(), "r");
    if (!pipe) {
        return;
    }
    std::string raw;
    char buffer[4096];
    while (fgets(buffer, sizeof(buffer), pipe)) {
        raw += buffer;
    }
    _pclose(pipe);

    // 7) Bỏ quotes đầu-cuối nếu có
    if (raw.size() >= 2 && raw.front() == '"' && raw.back() == '"') {
        raw = raw.substr(1, raw.size() - 2);
    }

    // 8) Unescape JSON inline
    std::string code;
    for (size_t i = 0; i < raw.size(); ++i) {
        if (raw[i] == '\\\\' && i + 1 < raw.size()) {
            ++i;
            char esc = raw[i];
            if (esc == 'n')      code += '\\n';
            else if (esc == 't') code += '\\t';
            else if (esc == '\\\\') code += '\\\\';
            else if (esc == '"')  code += '"';
            else                  code += esc;
        } else {
            code += raw[i];
        }
    }

    // 9) Ghi code ra file test.cpp
    std::ofstream out("test.cpp", std::ios::binary);
    out << code;
    out.close();
}`
}
  },
  methods: {
    ...mapActions(['fetchModels', 'fetchCredits']),
    generateCode() {
      if (!this.canGenerate) return;
      
      this.loading = true;
      this.error = null;
      
      // Import API config here to ensure it's correctly loaded
      import('@/utils/apiConfig').then(apiConfig => {
        const apiUrl = `${apiConfig.default.baseURL}/code/generate-code`;
        const token = localStorage.getItem('token');
        
        const requestData = {
          model_name: this.selectedModel,
          prompt: this.prompt
        };
        
        fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(requestData)
        })
          .then(response => {
            if (!response.ok) {
              return response.json().then(err => {
                throw new Error(err.detail || 'Failed to generate code');
              });
            }
            return response.json();
          })
          .then(data => {
            this.generatedCode = data.generated_code;
            this.fetchCredits(); // Update credits after generation
          })
          .catch(err => {
            console.error('Error:', err);
            this.error = err.response?.data?.detail || 'Code generation failed. Please try again.';
          })
          .finally(() => {
            this.loading = false;
          });
      });
    }
  },
  created() {
    this.fetchModels();
    this.fetchCredits();
  }
}
</script>

<style scoped>
.generate-code-page {
  position: relative;
  min-height: calc(100vh - 56px);
  padding: 20px 0;
  background-color: var(--dark-bg);
}

.blockchain-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: linear-gradient(rgba(65, 88, 208, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(65, 88, 208, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 0;
  pointer-events: none;
}

.page-title {
  color: var(--dark-text);
  font-weight: 600;
  font-size: 2.2rem;
  margin-bottom: 2rem;
  position: relative;
  display: inline-block;
}

.page-title:after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, #0070f3, #00c9ff);
  border-radius: 3px;
}

.credit-display {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.credit-icon {
  font-size: 2rem;
  margin-right: 1rem;
  color: #ffd700;
}

.credit-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.credit-amount {
  font-size: 1.8rem;
  font-weight: 700;
}

.generate-card, .result-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  background-color: var(--dark-card-bg);
}

.generate-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.generate-btn {
  background: linear-gradient(90deg, #0070f3, #00c9ff);
  border: none;
  font-weight: 500;
  font-size: 1.1rem;
  border-radius: 8px;
  padding: 12px 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.generate-btn:disabled {
  background: linear-gradient(90deg, #9e9e9e, #bdbdbd);
  cursor: not-allowed;
}

.result-card .card-header {
  background-color: var(--dark-card-secondary);
  border-bottom: 1px solid var(--dark-border);
  padding: 15px 20px;
  color: var(--dark-text);
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.15);
  color: #ff8896;
  border-color: rgba(220, 53, 69, 0.3);
  border-radius: 10px;
}
</style>