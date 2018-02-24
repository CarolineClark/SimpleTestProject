using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RotateAround : MonoBehaviour {
	public Vector3 centre;
	public float speed;
	private Light light;

	// Use this for initialization
	void Start () {
		light = GetComponent<Light> ();
	}
	
	// Update is called once per frame
	void Update () {
		light.transform.RotateAround(centre, Vector3.forward, speed * Time.deltaTime);
	}
}
