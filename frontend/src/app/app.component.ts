import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="min-h-screen bg-gray-50">
      <!-- Navigation -->
      <nav class="bg-white shadow-sm border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <h1 class="text-xl font-semibold text-gray-900">SBTM v2</h1>
            </div>
            <div class="flex items-center space-x-4">
              <a href="#" class="text-gray-600 hover:text-gray-900">Sessions</a>
              <a href="#" class="text-gray-600 hover:text-gray-900">Charters</a>
              <a href="#" class="text-gray-600 hover:text-gray-900">Dashboard</a>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <div class="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
            <div class="text-center">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">Welcome to SBTM v2</h2>
              <p class="text-gray-600 mb-6">Session-Based Test Management Tool</p>
              <div class="space-y-2">
                <p class="text-sm text-green-600">✅ FastAPI Backend Running</p>
                <p class="text-sm text-green-600">✅ Angular Frontend Working</p>
                <p class="text-sm text-blue-600">🚀 Ready for Development</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `,
  styles: []
})
export class AppComponent {
  title = 'sbtm-v2-frontend';
}