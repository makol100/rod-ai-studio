var viewer = pannellum.viewer('panorama', {
  default: { firstScene: 'parking', autoLoad: true, sceneFadeDuration: 900,
             autoRotate: -3, autoRotateInactivityDelay: 6000, hfov: 100 },
  scenes: {
    parking: {
      title: 'Parking',
      type: 'equirectangular',
      panorama: '/static/spacer/parking.jpg',
      hotSpots: [
        { pitch: -4, yaw: 118, type: 'scene', cssClass: 'strzalka', text: 'Przejdź na plac zabaw ➜', sceneId: 'plac', targetYaw: 95, targetPitch: 0 }
      ]
    },
    plac: {
      title: 'Plac zabaw',
      type: 'equirectangular',
      panorama: '/static/spacer/plac.jpg',
      hotSpots: [
        { pitch: -4, yaw: 95, type: 'scene', cssClass: 'strzalka', text: '➜ Wróć na parking', sceneId: 'parking', targetYaw: 118, targetPitch: 0 }
      ]
    }
  }
});
