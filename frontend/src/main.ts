import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

console.log('Starting SBTM v2 Angular app...');

bootstrapApplication(AppComponent, appConfig)
  .then(() => console.log('App started successfully!'))
  .catch((err) => {
    console.error('App failed to start:', err);
    document.body.innerHTML = '<h1 style="color: red;">Error: ' + err.message + '</h1>';
  });