import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobAnalyzer } from './job-analyzer';

describe('JobAnalyzer', () => {
  let component: JobAnalyzer;
  let fixture: ComponentFixture<JobAnalyzer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobAnalyzer],
    }).compileComponents();

    fixture = TestBed.createComponent(JobAnalyzer);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
