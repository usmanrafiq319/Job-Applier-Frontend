import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Outreach } from './outreach';

describe('Outreach', () => {
  let component: Outreach;
  let fixture: ComponentFixture<Outreach>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Outreach],
    }).compileComponents();

    fixture = TestBed.createComponent(Outreach);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
